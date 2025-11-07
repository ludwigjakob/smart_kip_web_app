import os
from data_connector.base_connector import BaseConnector
from dotenv import load_dotenv
import mysql.connector

load_dotenv()  # Lädt Umgebungsvariablen aus .env

class ModeConnector(BaseConnector):
    def __init__(self, name="mode", bucket=None):
        super().__init__(name, bucket)
        self.db_config = {
            'user': os.getenv('MARIADB_USER'),
            'password': os.getenv('MARIADB_PASSWORD'),
            'host': os.getenv('MARIADB_HOST'),
            'database': os.getenv('MARIADB_DBNAME')
        }

        self.ensure_database_exists()
        self.init_db()  # Datenbank beim Erstellen initialisieren

    def ensure_database_exists(self):
        """Stellt sicher, dass die Datenbank existiert, indem sie ggf. erstellt wird."""
        conn = mysql.connector.connect(
            user=self.db_config['user'],
            password=self.db_config['password'],
            host=self.db_config['host']
        )
        c = conn.cursor()
        c.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
        conn.close()

    def init_db(self):
        """Erstellt die Datenbanktabelle und initialisiert den Moduswert."""
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()

        # Tabelle erstellen, falls sie nicht existiert
        c.execute('''
            CREATE TABLE IF NOT EXISTS mode (
                id INT PRIMARY KEY,
                value VARCHAR(255) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Initialwert setzen, falls leer
        c.execute('SELECT COUNT(*) FROM mode')
        if c.fetchone()[0] == 0:
            c.execute('INSERT INTO mode (id, value) VALUES (1, %s)', ('auto',))

        conn.commit()
        conn.close()

    def read(self) -> str:
        """Lädt den aktuellen Moduswert aus der Datenbank."""
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()
        c.execute("SELECT value FROM mode WHERE id = 1")
        result = c.fetchone()
        conn.close()
        return result[0] if result else "auto"

    def write(self, mode: str):
        """Speichert einen neuen Moduswert in der Datenbank."""
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()
        c.execute("UPDATE mode SET value = %s, timestamp = CURRENT_TIMESTAMP WHERE id = 1", (mode,))
        conn.commit()
        conn.close()
