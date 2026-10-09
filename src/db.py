"""Модуль работы с базой данных SQLite."""
import sqlite3
import os
from src.config import DB_PATH


def get_connection():
    """Возвращает соединение с базой данных."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Создаёт таблицы, если их нет."""
    conn = get_connection()
    cursor = conn.cursor()
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processes (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            state TEXT DEFAULT 'ready',
            owner TEXT,
            memory_used INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            content TEXT,
            owner TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS syscalls_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            syscall_name TEXT NOT NULL,
            args TEXT,
            user TEXT,
            status TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"База данных инициализирована: {DB_PATH}")


def execute_query(sql, params=()):
    """Выполняет произвольный запрос."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    conn.close()
    return result


if __name__ == "__main__":
    os.makedirs("db", exist_ok=True)
    init_db()