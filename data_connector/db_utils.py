import mysql.connector

def ensure_database_exists(db_config: dict):
    """Stellt sicher, dass die Datenbank existiert, indem sie ggf. erstellt wird."""
    conn = mysql.connector.connect(
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host']
    )
    c = conn.cursor()
    c.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
    conn.close()