"""Модуль системных вызовов."""
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


def sys_echo(message, current_user="guest"):
    """Возвращает переданное сообщение."""
    log_syscall("sys_echo", message, current_user)
    return message


def sys_get_users(current_user="guest"):
    """Возвращает список пользователей."""
    log_syscall("sys_get_users", "", current_user)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, login, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


if __name__ == "__main__":
    print(sys_echo("Hello from kernel!"))
    print(sys_get_users())