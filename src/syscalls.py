"""Модуль системных вызовов."""

from src.db import get_connection
from src.auth import authenticate, check_permission
from src.kernel import kernel_instance
from src import fs, scheduler



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
    file_id = fs.create_file(path, content, current_user)
    if file_id == -1:
        log_syscall("sys_create_file", path, current_user, "EXISTS")
        return -1
    log_syscall("sys_create_file", path, current_user, "OK")
    return file_id


def sys_read_file(path, current_user="guest"):
    log_syscall("sys_read_file", path, current_user, "check")
    content = fs.read_file(path)
    log_syscall("sys_read_file", path, current_user, "OK")
    return content


def sys_delete_file(path, current_user="guest"):
    log_syscall("sys_delete_file", path, current_user, "check")
    owner = fs.get_owner(path)
    if owner is None:
        log_syscall("sys_delete_file", path, current_user, "NOT_FOUND")
        return False
    if not check_permission(current_user, "delete_file", owner):
        log_syscall("sys_delete_file", path, current_user, "DENIED")
        return False
    fs.delete_file(path)
    log_syscall("sys_delete_file", path, current_user, "OK")
    return True


def sys_list_files(path="/", current_user="guest"):
    log_syscall("sys_list_files", path, current_user, "OK")
    return fs.list_files(path)



def sys_exec(name, current_user="guest", memory_size=10):
    log_syscall("sys_exec", name, current_user, "check")
    pid = scheduler.create_process(name, current_user, memory_size)
    if pid == -1:
        log_syscall("sys_exec", name, current_user, "DENIED")
        return -1
    log_syscall("sys_exec", name, current_user, "OK")
    return pid


def sys_ps(current_user="guest"):
    log_syscall("sys_ps", "", current_user, "OK")
    return scheduler.list_processes()


def sys_kill(pid, current_user="guest"):
    log_syscall("sys_kill", str(pid), current_user, "check")
    if not check_permission(current_user, "kill"):
        log_syscall("sys_kill", str(pid), current_user, "DENIED")
        return False
    result = scheduler.terminate_process(pid)
    log_syscall("sys_kill", str(pid), current_user,
                "OK" if result else "NOT_FOUND")
    return result


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