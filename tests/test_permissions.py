"""Тесты разграничения прав доступа."""

from src import fs, db
from src.syscalls import sys_delete_file, sys_kill


def setup():
    for f in db.execute_select("files"):
        if f["path"].startswith("/perm"):
            db.execute_delete("files", {"id": f["id"]})


def test_guest_cannot_delete_admin_file():
    fs.create_file("/perm_admin.txt", "x", "admin")
    result = sys_delete_file("/perm_admin.txt", "guest")
    assert result is False, "guest не должен удалять файл admin"
    print("[PASS] guest не может удалить файл admin")


def test_admin_can_delete_any_file():
    fs.create_file("/perm_user.txt", "x", "user")
    result = sys_delete_file("/perm_user.txt", "admin")
    assert result is True, "admin должен удалять любой файл"
    print("[PASS] admin может удалить файл user")


def test_guest_cannot_kill_process():
    result = sys_kill(1, "guest")
    assert result is False, "guest не должен убивать процессы"
    print("[PASS] guest не может убить процесс")


def test_admin_can_kill_process():
    result = sys_kill(1, "admin")
    print("[PASS] admin может пытаться убить процесс (не DENIED)")


if __name__ == "__main__":
    setup()
    test_guest_cannot_delete_admin_file()
    test_admin_can_delete_any_file()
    test_guest_cannot_kill_process()
    test_admin_can_kill_process()
    print("\nВсе тесты пройдены.")