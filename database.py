import os
import sqlite3

from config import DB_PATH, DATA_DIR


def get_db():
    """
    Abre una conexión con la base de datos SQLite.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Crea las tablas necesarias si todavía no existen.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                original_url TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                scans INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                last_scan_at TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link_id INTEGER NOT NULL,
                scanned_at TEXT NOT NULL,
                ip TEXT,
                user_agent TEXT,
                FOREIGN KEY(link_id) REFERENCES links(id)
            )
        """)
