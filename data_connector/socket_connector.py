import os
from data_connector.base_connector import BaseConnector
from dotenv import load_dotenv
import mysql.connector
from data_connector.db_utils import ensure_database_exists

load_dotenv()

class SocketConnector(BaseConnector):
    def __init__(self, name="socket", bucket=None):
        super().__init__(name, bucket)
        self.db_config = {
            'user': os.getenv('MARIADB_USER'),
            'password': os.getenv('MARIADB_PASSWORD'),
            'host': os.getenv('MARIADB_HOST'),
            'database': os.getenv('MARIADB_DBNAME')
        }

        ensure_database_exists(self.db_config)
        self.init_db()

    def init_db(self):
        """Erstellt die Tabelle für genau eine Socket."""
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS socket (
                id INT PRIMARY KEY,
                state VARCHAR(10) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Initialwert setzen, falls leer
        c.execute('SELECT COUNT(*) FROM socket')
        if c.fetchone()[0] == 0:
            c.execute('INSERT INTO socket (id, state) VALUES (1, "off")')

        conn.commit()
        conn.close()

    def read(self) -> dict:
        """Liest den aktuellen Zustand der einzigen Socket."""
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()
        c.execute("SELECT state FROM socket WHERE id = 1")
        result = c.fetchone()
        conn.close()
        if result:
            return {"state": result[0]}
        return {"state": "off"}

    def write(self, state: str):
        """Schreibt den Zustand der einzigen Socket."""
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()
        c.execute(
            "UPDATE socket SET state = %s, timestamp = CURRENT_TIMESTAMP WHERE id = 1",
            (state,)
        )
        conn.commit()
        conn.close()