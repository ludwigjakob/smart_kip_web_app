import os
from data_connector.base_connector import BaseConnector
from dotenv import load_dotenv
import mysql.connector
from data_connector.db_utils import ensure_database_exists


load_dotenv()  # Lädt Umgebungsvariablen aus .env

class AnalysisConnector(BaseConnector):
    def __init__(self, name="analysis", bucket=None):
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
            CREATE TABLE IF NOT EXISTS analysis_settings (
                id INT PRIMARY KEY DEFAULT 1,
                mode BOOLEAN NOT NULL,
                interval_days INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def write(self, data: dict):
        mode = bool(data.get("mode", False))
        interval_days = int(data.get("interval_days", 1))

        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor()
        c.execute("""
            INSERT INTO analysis_settings (id, mode, interval_days)
            VALUES (1, %s, %s)
            ON DUPLICATE KEY UPDATE mode = %s, interval_days = %s
        """, (mode, interval_days, mode, interval_days))
        conn.commit()
        conn.close()


    def read(self):
        conn = mysql.connector.connect(**self.db_config)
        c = conn.cursor(dictionary=True)
        c.execute("SELECT mode, interval_days FROM analysis_settings WHERE id = 1")
        result = c.fetchone()
        conn.close()
        return result or {"mode": 0, "interval_days": 1}
