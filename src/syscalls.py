"""Модуль системных вызовов."""
from src.logger import log_syscall
from src.auth import authenticate, check_permission
from src.kernel import kernel_instance
from src import fs, scheduler


def sys_login(login, password, current_user="guest"):
    """Вход в систему."""
    log_syscall("sys_login", login, current_user, "check")
    user = authenticate(login, password)
    if user:
        kernel_instance.set_user(login)
        log_syscall("sys_login", login, current_user, "OK")
        return True
    log_syscall("sys_login", login, current_user, "DENIED")
    return False


def sys_logout(current_user="guest"):
    """Выход из системы."""
    log_syscall("sys_logout", "", current_user)
    kernel_instance.set_user("guest")
    return True


def sys_whoami(current_user="guest"):
    """Возвращает текущего пользователя."""
    log_syscall("sys_whoami", "", current_user, "OK")
    return kernel_instance.get_user()


def sys_create_file(path, content, current_user="guest"):
    """Создание файла."""
    log_syscall("sys_create_file", path, current_user, "check")
    file_id = fs.create_file(path, content, current_user)
    if file_id == -1:
        log_syscall("sys_create_file", path, current_user, "EXISTS")
        return -1
    log_syscall("sys_create_file", path, current_user, "OK")
    return file_id


def sys_read_file(path, current_user="guest"):
    """Чтение файла."""
    log_syscall("sys_read_file", path, current_user, "check")
    content = fs.read_file(path)
    log_syscall("sys_read_file", path, current_user, "OK")
    return content


def sys_delete_file(path, current_user="guest"):
    """Удаление файла с проверкой прав."""
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


def sys_list_files(prefix="", current_user="guest"):
    """Список файлов."""
    log_syscall("sys_list_files", prefix, current_user, "OK")
    return fs.list_files(prefix)


def sys_exec(name, current_user="guest"):
    """Запуск процесса."""
    log_syscall("sys_exec", name, current_user, "check")
    pid = scheduler.create_process(name, current_user)
    if pid == -1:
        log_syscall("sys_exec", name, current_user, "NO_MEMORY")
        return -1
    log_syscall("sys_exec", name, current_user, "OK")
    return pid


def sys_ps(current_user="guest"):
    """Список процессов."""
    log_syscall("sys_ps", "", current_user, "OK")
    return scheduler.list_processes()


def sys_kill(pid, current_user="guest"):
    """Завершение процесса."""
    log_syscall("sys_kill", str(pid), current_user, "check")
    if not check_permission(current_user, "kill"):
        log_syscall("sys_kill", str(pid), current_user, "DENIED")
        return False
    result = scheduler.terminate_process(pid)
    log_syscall("sys_kill", str(pid), current_user, "OK" if result else "NOT_FOUND")
    return result


def sys_mem_alloc(size, current_user="guest"):
    """Выделение памяти."""
    log_syscall("sys_mem_alloc", str(size), current_user)
    return size


def sys_logs(limit, current_user="guest"):
    """Получение журнала."""
    log_syscall("sys_logs", str(limit), current_user)
    return []


def sys_shutdown(current_user="guest"):
    """Завершение работы."""
    log_syscall("sys_shutdown", "", current_user)
    return True


if __name__ == "__main__":
    print(sys_login("admin", "secret"))
    print(sys_whoami("admin"))
    print(sys_create_file("/test.txt", "hello", "admin"))
    print(sys_ps("admin"))