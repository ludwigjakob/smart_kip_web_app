# mode_database.py
import sqlite3
import os

DB_PATH = 'mode.db'  # Die Datenbank liegt lokal im Projektverzeichnis

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS mode (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            value TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('SELECT COUNT(*) FROM mode')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO mode (id, value) VALUES (1, ?)', ('auto',))
    conn.commit()
    conn.close()

def save_mode_to_db(mode):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE mode SET value = ?, timestamp = CURRENT_TIMESTAMP WHERE id = 1', (mode,))
    conn.commit()
    conn.close()

def load_latest_mode():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT value FROM mode WHERE id = 1')
    result = c.fetchone()
    conn.close()
    return result[0] if result else 'auto'
