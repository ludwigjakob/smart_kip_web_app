import os
from data_connector.base_connector import BaseConnector
from dotenv import load_dotenv
import mysql.connector
from data_connector.db_utils import ensure_database_exists
import threading
import time



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

        ensure_database_exists(self.db_config)
        self.init_db()  # Datenbank beim Erstellen initialisieren

    def init_db(self):
        """Erstellt die Datenbanktabelle und initialisiert den Moduswert."""
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()

        # Tabelle erstellen, falls sie nicht existiert
        c.execute('''
            CREATE TABLE IF NOT EXISTS mode (
                id INT PRIMARY KEY,
                value VARCHAR(255) NOT NULL,
                fan_speed INT DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Initialwert setzen, falls leer
        c.execute('SELECT COUNT(*) FROM mode')
        if c.fetchone()[0] == 0:
            c.execute('INSERT INTO mode (id, value) VALUES (1, %s)', ('auto',))

        conn.commit()
        conn.close()

    def read(self) -> dict:
        """Lädt den aktuellen Modus und die Lüftergeschwindigkeit aus der Datenbank."""
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()
        c.execute("SELECT value, fan_speed FROM mode WHERE id = 1")
        result = c.fetchone()
        conn.close()
        if result:
            return {"mode": result[0], "fan_speed": result[1]}
        return {"mode": "auto", "fan_speed": 0}

    def write(self, mode: str):
        """Speichert einen neuen Moduswert in der Datenbank."""
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()
        c.execute("UPDATE mode SET value = %s, timestamp = CURRENT_TIMESTAMP WHERE id = 1", (mode,))
        conn.commit()
        conn.close()

    def write_fan_speed(self, speed: int):
        """Speichert die Lüftergeschwindigkeit verzögert in der Datenbank."""
        def delayed_write():
            time.sleep(0.5)
            conn = mysql.connector.connect(**self.db_config)
            c = conn.cursor()
            c.execute("UPDATE mode SET fan_speed = %s, timestamp = CURRENT_TIMESTAMP WHERE id = 1", (speed,))
            conn.commit()
            conn.close()

        threading.Thread(target=delayed_write).start()

