"""Тесты аутентификации."""

from src import db
from src.auth import hash_password, register_user, authenticate, check_permission


def setup():
    for u in ("test1", "test2"):
        db.execute_delete("users", {"login": u})


def test_hash():
    h = hash_password("secret")
    assert len(h) == 64
    assert h != "secret"
    print("[PASS] пароль хэшируется")


def test_register_unique():
    register_user("test1", "pass1234", "user")
    result = register_user("test1", "pass5678", "user")
    assert result is None
    print("[PASS] дубликат логина отклонён")


def test_authenticate():
    register_user("test2", "pass1234", "user")
    assert authenticate("test2", "pass1234") is not None
    assert authenticate("test2", "wrong") is None
    print("[PASS] вход проверяется")


def test_admin_permission():
    assert check_permission("admin", "delete_file", "user") is True
    assert check_permission("user", "delete_file", "admin") is False
    print("[PASS] права разграничены")


if __name__ == "__main__":
    setup()
    test_hash()
    test_register_unique()
    test_authenticate()
    test_admin_permission()
    print("\nВсе тесты auth пройдены.")