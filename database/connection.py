import os
import sqlite3

DB_FILE = os.getenv("DB_FILE", "weaver.db")

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT, 
            provider TEXT NOT NULL,
            provider_id TEXT UNIQUE NOT NULL,
            is_vip INTEGER DEFAULT 0 NOT NULL
        );
                         
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            user_email TEXT NOT NULL,
            FOREIGN KEY(user_email) REFERENCES users(email) 
        );
    """)

    conn.commit()
    conn.close()