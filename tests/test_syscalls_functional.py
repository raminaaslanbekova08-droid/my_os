"""Функциональные тесты системных вызовов."""

from src import db
from src.auth import register_user
from src.kernel import kernel_instance
from src.syscalls import (
    sys_login, sys_create_file, sys_read_file, sys_delete_file,
    sys_list_files, sys_exec, sys_kill, sys_logs,
)


def setup():
    for u in ("st_admin", "st_user"):
        db.execute_delete("users", {"login": u})
    register_user("st_admin", "secret123", "admin")
    register_user("st_user", "user1234", "user")
    for f in db.execute_select("files"):
        if f["path"].startswith("/st"):
            db.execute_delete("files", {"id": f["id"]})
    for p in db.execute_select("processes"):
        db.execute_delete("processes", {"pid": p["pid"]})
    kernel_instance.reset()


def count_logs(name):
    return len(db.execute_select("syscalls_log", {"syscall_name": name}))


def test_sys_login_logs():
    before = count_logs("sys_login")
    sys_login("st_admin", "secret123")
    assert count_logs("sys_login") == before + 2
    print("[PASS] sys_login логируется")


def test_sys_create_file_logs():
    before = count_logs("sys_create_file")
    sys_create_file("/st01.txt", "x", "st_admin")
    assert count_logs("sys_create_file") == before + 2
    print("[PASS] sys_create_file логируется")


def test_sys_create_file_content():
    fid = sys_create_file("/st02.txt", "content", "st_admin")
    assert fid > 0
    assert sys_read_file("/st02.txt", "st_admin") == "content"
    print("[PASS] sys_create_file с содержимым")


def test_sys_delete_denied_for_user():
    sys_create_file("/st03.txt", "x", "st_admin")
    assert sys_delete_file("/st03.txt", "st_user") is False
    print("[PASS] sys_delete_file запрещён user")


def test_sys_delete_allowed_for_admin():
    sys_create_file("/st04.txt", "x", "st_user")
    assert sys_delete_file("/st04.txt", "st_admin") is True
    print("[PASS] sys_delete_file разрешён admin")


def test_sys_delete_logs_denied():
    sys_create_file("/st05.txt", "x", "st_admin")
    before = len(db.execute_select("syscalls_log", {"status": "DENIED"}))
    sys_delete_file("/st05.txt", "st_user")
    after = len(db.execute_select("syscalls_log", {"status": "DENIED"}))
    assert after > before
    print("[PASS] отказ в правах логируется со статусом DENIED")


def test_sys_list_files():
    sys_create_file("/st06_a.txt", "a", "st_admin")
    sys_create_file("/st06_b.txt", "b", "st_admin")
    files = sys_list_files("/st06", "st_admin")
    assert "/st06_a.txt" in files
    print("[PASS] sys_list_files возвращает список")


def test_sys_exec_logs():
    before = count_logs("sys_exec")
    pid = sys_exec("st_app", "st_admin")
    assert pid > 0
    assert count_logs("sys_exec") == before + 2
    print("[PASS] sys_exec логируется")


def test_sys_kill_denied_for_user():
    pid = sys_exec("st_temp", "st_admin")
    assert sys_kill(pid, "st_user") is False
    print("[PASS] sys_kill запрещён user")


def test_sys_kill_allowed_for_admin():
    pid = sys_exec("st_temp2", "st_admin")
    assert sys_kill(pid, "st_admin") is True
    print("[PASS] sys_kill разрешён admin")


def test_sys_logs_returns_list():
    logs = sys_logs(10, "st_admin")
    assert isinstance(logs, list)
    print("[PASS] sys_logs возвращает список")


if __name__ == "__main__":
    setup()
    test_sys_login_logs()
    test_sys_create_file_logs()
    test_sys_create_file_content()
    test_sys_delete_denied_for_user()
    test_sys_delete_allowed_for_admin()
    test_sys_delete_logs_denied()
    test_sys_list_files()
    test_sys_exec_logs()
    test_sys_kill_denied_for_user()
    test_sys_kill_allowed_for_admin()
    test_sys_logs_returns_list()
    print("\nВсе функциональные тесты syscalls пройдены.")