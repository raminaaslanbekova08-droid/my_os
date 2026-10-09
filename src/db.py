"""Слой работы с базой данных SQLite."""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "os.sqlite")


def get_connection():
    """Возвращает соединение с базой данных."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Создаёт все таблицы, если их ещё нет."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processes (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            state TEXT NOT NULL DEFAULT 'ready',
            owner TEXT NOT NULL,
            memory_used INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            content TEXT,
            owner TEXT NOT NULL,
            is_directory INTEGER NOT NULL DEFAULT 0,
            parent_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS syscalls_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            syscall_name TEXT NOT NULL,
            args TEXT,
            user TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            used INTEGER NOT NULL DEFAULT 0,
            limit_value INTEGER NOT NULL DEFAULT 1024
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    for role in ("admin", "user", "guest"):
        cursor.execute("INSERT OR IGNORE INTO roles (name) VALUES (?)", (role,))

    conn.commit()
    conn.close()


def execute_insert(table, data):
    """Вставляет запись. data — словарь {поле: значение}. Возвращает id."""
    keys = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    sql = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, tuple(data.values()))
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def execute_select(table, conditions=None):
    """Возвращает список записей."""
    sql = f"SELECT * FROM {table}"
    params = ()

    if conditions:
        where = " AND ".join([f"{k} = ?" for k in conditions.keys()])
        sql += f" WHERE {where}"
        params = tuple(conditions.values())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return result


def execute_update(table, data, conditions):
    """Обновляет записи по условию."""
    set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
    where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
    sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, tuple(data.values()) + tuple(conditions.values()))
    conn.commit()
    conn.close()


def execute_delete(table, conditions):
    """Удаляет записи по условию."""
    if not conditions:
        sql = f"DELETE FROM {table}"
        params = ()
    else:
        where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        params = tuple(conditions.values())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"База данных инициализирована: {DB_PATH}")