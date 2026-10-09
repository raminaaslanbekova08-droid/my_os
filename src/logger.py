"""Модуль журналирования системных вызовов."""
from src.db import get_connection


def log_syscall(name, args="", user="system", status="OK"):
    """Записывает системный вызов в журнал."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO syscalls_log (syscall_name, args, user, status) VALUES (?, ?, ?, ?)",
        (name, args, user, status)
    )
    conn.commit()
    conn.close()