import sqlite3

DB_FILE = "weaver.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT, 
            provider TEXT NOT NULL,
            provider_id TEXT UNIQUE NOT NULL,
            is_vip INTEGER DEFAULT 0 NOT NULL
        )
    """)

    conn.commit()
    conn.close()