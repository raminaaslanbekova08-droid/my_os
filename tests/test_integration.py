"""Интеграционные тесты учебной ОС."""

from src import db
from src.auth import register_user
from src.kernel import kernel_instance
from src.syscalls import (
    sys_login, sys_create_file, sys_read_file, sys_delete_file,
    sys_exec, sys_kill,
)


def setup():
    for u in ("int_admin", "int_user"):
        db.execute_delete("users", {"login": u})
    register_user("int_admin", "secret123", "admin")
    register_user("int_user", "user1234", "user")

    for f in db.execute_select("files"):
        if f["path"].startswith("/int"):
            db.execute_delete("files", {"id": f["id"]})

    for p in db.execute_select("processes"):
        kernel_instance.free_memory(p["memory_used"])
        db.execute_delete("processes", {"pid": p["pid"]})

    kernel_instance.reset()


def test_is01_create_file():
    sys_login("int_admin", "secret123")
    fid = sys_create_file("/int01.txt", "content", "int_admin")
    assert fid > 0
    print("[PASS] IS-01: создание файла")


def test_is02_read_file():
    sys_login("int_admin", "secret123")
    sys_create_file("/int02.txt", "hello", "int_admin")
    assert sys_read_file("/int02.txt", "int_admin") == "hello"
    print("[PASS] IS-02: чтение файла")


def test_is03_delete_denied():
    sys_login("int_admin", "secret123")
    sys_create_file("/int03.txt", "x", "int_admin")
    result = sys_delete_file("/int03.txt", "int_user")
    assert result is False
    print("[PASS] IS-03: отказ в удалении чужого файла")


def test_is04_run_process():
    sys_login("int_admin", "secret123")
    before = kernel_instance.memory_used
    pid = sys_exec("int04_app", "int_admin")
    assert pid > 0
    assert kernel_instance.memory_used > before
    print("[PASS] IS-04: запуск процесса")


def test_is05_kill_process():
    sys_login("int_admin", "secret123")
    pid = sys_exec("int05_app", "int_admin")
    used = kernel_instance.memory_used
    assert sys_kill(pid, "int_admin") is True
    assert kernel_instance.memory_used < used
    print("[PASS] IS-05: завершение процесса")


def test_is06_full_admin_scenario():
    sys_login("int_admin", "secret123")
    fid = sys_create_file("/int06.txt", "admin data", "int_admin")
    pid = sys_exec("int06_app", "int_admin")
    assert fid > 0 and pid > 0
    assert sys_read_file("/int06.txt", "int_admin") == "admin data"
    assert sys_kill(pid, "int_admin") is True
    print("[PASS] IS-06: сквозной сценарий администратора")


def test_is07_user_scenario():
    sys_login("int_user", "user1234")
    sys_create_file("/int07_user.txt", "user data", "int_user")
    sys_create_file("/int07_admin.txt", "admin data", "int_admin")
    assert sys_delete_file("/int07_user.txt", "int_user") is True
    assert sys_delete_file("/int07_admin.txt", "int_user") is False
    print("[PASS] IS-07: сценарий обычного пользователя")


if __name__ == "__main__":
    setup()
    test_is01_create_file()
    test_is02_read_file()
    test_is03_delete_denied()
    test_is04_run_process()
    test_is05_kill_process()
    test_is06_full_admin_scenario()
    test_is07_user_scenario()
    print("\nВсе интеграционные тесты пройдены.")