import os
from data_connector.base_connector import BaseConnector
from dotenv import load_dotenv
import mysql.connector
from data_connector.db_utils import ensure_database_exists


load_dotenv()  # Lädt Umgebungsvariablen aus .env

class ThresholdConnector(BaseConnector):
    def __init__(self, name="threshold", bucket=None):
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
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS thresholds (
                level INT PRIMARY KEY,
                value FLOAT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def read(self) -> dict:
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()
        c.execute("SELECT level, value FROM thresholds")
        result = {level: value for level, value in c.fetchall()}
        conn.close()
        return result

    def write(self, level_or_dict, value: float = None):
        """
        Speichert entweder einen einzelnen Schwellenwert (level, value)
        oder mehrere Schwellenwerte als Dictionary {level: value}.
        """
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()

        if isinstance(level_or_dict, dict):
            for level, val in level_or_dict.items():
                c.execute("""
                    INSERT INTO thresholds (level, value)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE value = %s
                """, (level, val, val))
        else:
            c.execute("""
                INSERT INTO thresholds (level, value)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE value = %s
            """, (level_or_dict, value, value))

        conn.commit()
        conn.close()
