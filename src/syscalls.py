"""Модуль системных вызовов."""

from src.db import get_connection
from src.auth import authenticate, check_permission
from src.kernel import kernel_instance



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


def sys_login(login, password, current_user="guest"):
    log_syscall("sys_login", login, current_user, "check")
    user = authenticate(login, password)
    if user:
        kernel_instance.set_user(login)
        log_syscall("sys_login", login, current_user, "OK")
        return True
    log_syscall("sys_login", login, current_user, "DENIED")
    return False


def sys_logout(current_user="guest"):
    log_syscall("sys_logout", "", current_user, "OK")
    kernel_instance.set_user("guest")
    return True


def sys_whoami(current_user="guest"):
    log_syscall("sys_whoami", "", current_user, "OK")
    return kernel_instance.get_user()



def sys_create_file(path, content, current_user="guest"):
    log_syscall("sys_create_file", path, current_user, "check")
    log_syscall("sys_create_file", path, current_user, "OK")
    return 1


def sys_read_file(path, current_user="guest"):
    log_syscall("sys_read_file", path, current_user, "check")
    log_syscall("sys_read_file", path, current_user, "OK")
    return ""


def sys_delete_file(path, current_user="guest", owner=None):
    log_syscall("sys_delete_file", path, current_user, "check")
    if not check_permission(current_user, "delete_file", owner):
        log_syscall("sys_delete_file", path, current_user, "DENIED")
        return False
    log_syscall("sys_delete_file", path, current_user, "OK")
    return True


def sys_list_files(path="/", current_user="guest"):
    log_syscall("sys_list_files", path, current_user, "OK")
    return []



def sys_exec(name, current_user="guest", memory_size=10):
    log_syscall("sys_exec", name, current_user, "check")
    log_syscall("sys_exec", name, current_user, "OK")
    return 42


def sys_ps(current_user="guest"):
    log_syscall("sys_ps", "", current_user, "OK")
    return []


def sys_kill(pid, current_user="guest"):
    log_syscall("sys_kill", str(pid), current_user, "check")
    if not check_permission(current_user, "kill"):
        log_syscall("sys_kill", str(pid), current_user, "DENIED")
        return False
    log_syscall("sys_kill", str(pid), current_user, "OK")
    return True


def sys_mem_alloc(size, current_user="guest"):
    log_syscall("sys_mem_alloc", str(size), current_user, "check")
    ok = kernel_instance.allocate_memory(size)
    log_syscall("sys_mem_alloc", str(size), current_user,
                "OK" if ok else "DENIED")
    return 0 if ok else -1


def sys_logs(limit=10, current_user="guest"):
    log_syscall("sys_logs", str(limit), current_user, "OK")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM syscalls_log ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def sys_shutdown(current_user="guest"):
    log_syscall("sys_shutdown", "", current_user, "OK")
    return True


if __name__ == "__main__":
    print("sys_login (admin/secret):", sys_login("admin", "secret"))
    print("sys_whoami:", sys_whoami("admin"))
    print("sys_login (wrong):", sys_login("admin", "wrong"))
    print("sys_delete_file (guest -> admin):",
          sys_delete_file("/admin.txt", "guest", owner="admin"))
    print("sys_kill (guest):", sys_kill(1, "guest"))
    print("Готово.")