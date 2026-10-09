"""Модуль системных вызовов.

Предоставляет единый интерфейс для оболочки.
Каждая функция:
  - логирует вызов в таблицу syscalls_log;
  - возвращает правдоподобный результат (заглушка).
"""

from src.db import get_connection



def log_syscall(name, args="", user="system", status="OK"):
    """Записывает информацию о системном вызове в таблицу syscalls_log."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO syscalls_log (syscall_name, args, user, status) "
        "VALUES (?, ?, ?, ?)",
        (name, str(args), user, status)
    )
    conn.commit()
    conn.close()



def check_permission(current_user, action, target_owner=None):
    """Проверяет, имеет ли пользователь право на действие.

    admin может всё.
    Обычный пользователь не может удалять чужие файлы и завершать процессы.
    """
    if current_user == "admin":
        return True

    if action == "delete_file" and target_owner and target_owner != current_user:
        return False

    if action == "kill" and current_user != "admin":
        return False

    return True


def sys_login(login, password, current_user="guest"):
    """Заглушка входа в систему. Возвращает True при успехе."""
    log_syscall("sys_login", login, current_user, "check")
    log_syscall("sys_login", login, current_user, "OK")
    return True


def sys_logout(current_user="guest"):
    """Заглушка выхода из системы."""
    log_syscall("sys_logout", "", current_user, "OK")
    return True


def sys_whoami(current_user="guest"):
    """Возвращает имя текущего пользователя."""
    log_syscall("sys_whoami", "", current_user, "OK")
    return current_user


def sys_create_file(path, content, current_user="guest"):
    """Заглушка создания файла. Возвращает id (пока всегда 1)."""
    log_syscall("sys_create_file", path, current_user, "check")
    log_syscall("sys_create_file", path, current_user, "OK")
    return 1


def sys_read_file(path, current_user="guest"):
    """Заглушка чтения файла. Возвращает пустую строку."""
    log_syscall("sys_read_file", path, current_user, "check")
    log_syscall("sys_read_file", path, current_user, "OK")
    return ""


def sys_delete_file(path, current_user="guest", owner=None):
    """Заглушка удаления файла с проверкой прав."""
    log_syscall("sys_delete_file", path, current_user, "check")

    if not check_permission(current_user, "delete_file", owner):
        log_syscall("sys_delete_file", path, current_user, "DENIED")
        return False

    log_syscall("sys_delete_file", path, current_user, "OK")
    return True


def sys_list_files(path="/", current_user="guest"):
    """Заглушка списка файлов. Возвращает пустой список."""
    log_syscall("sys_list_files", path, current_user, "OK")
    return []



def sys_exec(name, current_user="guest", memory_size=10):
    """Заглушка запуска процесса. Возвращает фиктивный PID = 42."""
    log_syscall("sys_exec", name, current_user, "check")
    log_syscall("sys_exec", name, current_user, "OK")
    return 42


def sys_ps(current_user="guest"):
    """Заглушка списка процессов. Возвращает пустой список."""
    log_syscall("sys_ps", "", current_user, "OK")
    return []


def sys_kill(pid, current_user="guest"):
    """Заглушка завершения процесса с проверкой прав."""
    log_syscall("sys_kill", str(pid), current_user, "check")

    if not check_permission(current_user, "kill"):
        log_syscall("sys_kill", str(pid), current_user, "DENIED")
        return False

    log_syscall("sys_kill", str(pid), current_user, "OK")
    return True



def sys_mem_alloc(size, current_user="guest"):
    """Заглушка выделения памяти. Возвращает 0 (успех)."""
    log_syscall("sys_mem_alloc", str(size), current_user, "check")
    log_syscall("sys_mem_alloc", str(size), current_user, "OK")
    return 0


def sys_logs(limit=10, current_user="guest"):
    """Заглушка чтения журнала. Возвращает пустой список."""
    log_syscall("sys_logs", str(limit), current_user, "OK")
    return []


def sys_shutdown(current_user="guest"):
    """Заглушка завершения работы ОС."""
    log_syscall("sys_shutdown", "", current_user, "OK")
    return True



if __name__ == "__main__":
    print("sys_login:", sys_login("admin", "secret"))
    print("sys_whoami:", sys_whoami("admin"))
    print("sys_create_file:", sys_create_file("/test.txt", "hello", "admin"))
    print("sys_ps:", sys_ps("admin"))
    print("sys_read_file:", repr(sys_read_file("/test.txt", "admin")))
    print("sys_list_files:", sys_list_files("/", "admin"))
    print("sys_exec:", sys_exec("app", "admin"))
    print("sys_kill:", sys_kill(42, "admin"))
    print("sys_kill (guest):", sys_kill(42, "guest"))
    print("sys_delete_file (guest -> admin):",
          sys_delete_file("/admin.txt", "guest", owner="admin"))
    print("sys_logs:", sys_logs(5, "admin"))
    print("sys_shutdown:", sys_shutdown("admin"))
    print("Готово.")