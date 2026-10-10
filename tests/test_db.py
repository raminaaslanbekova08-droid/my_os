"""Модульные тесты слоя данных."""

from src import db


def setup():
    db.execute_delete("users", {"login": "db_test"})


def test_insert():
    uid = db.execute_insert("users", {
        "login": "db_test", "password_hash": "x", "role": "user"
    })
    assert uid > 0
    print(f"[PASS] TC-01: создание записи, id={uid}")


def test_select():
    users = db.execute_select("users", {"login": "db_test"})
    assert len(users) == 1
    assert users[0]["login"] == "db_test"
    print("[PASS] TC-02: выборка по условию")


def test_select_all():
    users = db.execute_select("users")
    assert isinstance(users, list)
    print("[PASS] выборка всех записей")


def test_update():
    db.execute_update("users", {"role": "admin"}, {"login": "db_test"})
    users = db.execute_select("users", {"login": "db_test"})
    assert users[0]["role"] == "admin"
    print("[PASS] TC-03: обновление записи")


def test_delete():
    db.execute_delete("users", {"login": "db_test"})
    users = db.execute_select("users", {"login": "db_test"})
    assert len(users) == 0
    print("[PASS] TC-04: удаление записи")


def test_select_empty():
    users = db.execute_select("users", {"login": "nonexistent_user_xyz"})
    assert users == []
    print("[PASS] выборка несуществующего возвращает пустой список")


if __name__ == "__main__":
    setup()
    test_insert()
    test_select()
    test_select_all()
    test_update()
    test_delete()
    test_select_empty()
    print("\nВсе тесты db.py пройдены.")