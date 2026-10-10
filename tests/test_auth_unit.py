"""Модульные тесты auth."""

from src import db
from src.auth import hash_password, register_user, authenticate, check_permission


def setup():
    for u in ("au_test1", "au_test2"):
        db.execute_delete("users", {"login": u})


def test_hash():
    h = hash_password("secret")
    assert len(h) == 64
    assert h != "secret"
    print("[PASS] TC-08: хэширование пароля")


def test_register_unique():
    register_user("au_test1", "pass1234", "user")
    result = register_user("au_test1", "other1234", "user")
    assert result is None
    print("[PASS] TC-09: уникальность логина")


def test_authenticate():
    register_user("au_test2", "pass1234", "user")
    assert authenticate("au_test2", "pass1234") is not None
    assert authenticate("au_test2", "wrong") is None
    print("[PASS] TC-10: проверка входа")


def test_admin_permission():
    assert check_permission("admin", "kill") is True
    assert check_permission("user", "kill") is False
    print("[PASS] TC-11: разграничение прав")


if __name__ == "__main__":
    setup()
    test_hash()
    test_register_unique()
    test_authenticate()
    test_admin_permission()
    print("\nВсе тесты auth пройдены.")