"""Тесты файловой системы."""

from src import fs, db


def setup():
    """Удаляем все тестовые файлы с префиксом /t."""
    for f in db.execute_select("files"):
        if f["path"].startswith("/t"):
            db.execute_delete("files", {"id": f["id"]})


def test_create_and_read():
    fs.create_file("/t1.txt", "content1", "admin")
    assert fs.read_file("/t1.txt") == "content1"
    print("[PASS] создание и чтение файла")


def test_duplicate_path():
    fs.create_file("/t2.txt", "a", "admin")
    result = fs.create_file("/t2.txt", "b", "admin")
    assert result == -1
    print("[PASS] дубликат пути отклонён")


def test_update():
    fs.create_file("/t3.txt", "old", "admin")
    fs.write_file("/t3.txt", "new")
    assert fs.read_file("/t3.txt") == "new"
    print("[PASS] обновление содержимого")


def test_delete():
    fs.create_file("/t4.txt", "x", "admin")
    fs.delete_file("/t4.txt")
    assert fs.read_file("/t4.txt") == ""
    print("[PASS] удаление файла")


def test_owner():
    fs.create_file("/t5.txt", "x", "admin")
    assert fs.get_owner("/t5.txt") == "admin"
    assert fs.get_owner("/missing.txt") is None
    print("[PASS] получение владельца")


def test_list():
    fs.create_file("/t_list1.txt", "a", "admin")
    fs.create_file("/t_list2.txt", "b", "admin")
    files = fs.list_files("/t_list")
    assert "/t_list1.txt" in files
    assert "/t_list2.txt" in files
    print("[PASS] список файлов по префиксу")


if __name__ == "__main__":
    setup()
    test_create_and_read()
    test_duplicate_path()
    test_update()
    test_delete()
    test_owner()
    test_list()
    print("\nВсе тесты файловой системы пройдены.")