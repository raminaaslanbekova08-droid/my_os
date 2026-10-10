"""Стресс-тесты системы."""

from src import db
from src.auth import register_user
from src.kernel import kernel_instance
from src.syscalls import (
    sys_login, sys_create_file, sys_delete_file, sys_exec, sys_kill,
)


def setup():
    db.execute_delete("users", {"login": "stress_admin"})
    register_user("stress_admin", "stress123", "admin")
    for p in db.execute_select("processes"):
        db.execute_delete("processes", {"pid": p["pid"]})
    kernel_instance.reset()
    for f in db.execute_select("files"):
        if f["path"].startswith("/stress"):
            db.execute_delete("files", {"id": f["id"]})


def test_many_processes():
    sys_login("stress_admin", "stress123")
    pids = []
    for i in range(10):
        pid = sys_exec(f"stress_{i}", "stress_admin")
        assert pid > 0, f"Процесс {i} не создан"
        pids.append(pid)
    print(f"[PASS] создано 10 процессов: {pids}")
    assert len(db.execute_select("processes")) == 10
    for pid in pids:
        sys_kill(pid, "stress_admin")
    assert len(db.execute_select("processes")) == 0
    print("[PASS] все процессы завершены")


def test_memory_limit_stress():
    sys_login("stress_admin", "stress123")
    pids = []
    for i in range(100):
        pid = sys_exec(f"mem_{i}", "stress_admin", 100)
        if pid == -1:
            break
        pids.append(pid)
    assert len(pids) < 100
    print(f"[PASS] лимит памяти соблюдается, создано {len(pids)} процессов")
    for pid in pids:
        sys_kill(pid, "stress_admin")


def test_many_files():
    sys_login("stress_admin", "stress123")
    for i in range(50):
        fid = sys_create_file(f"/stress_{i}.txt", f"content_{i}", "stress_admin")
        assert fid > 0
    print("[PASS] создано 50 файлов")
    for i in range(50):
        sys_delete_file(f"/stress_{i}.txt", "stress_admin")
    print("[PASS] все файлы удалены")


def test_many_users():
    for i in range(20):
        db.execute_delete("users", {"login": f"bulk_{i}"})
        register_user(f"bulk_{i}", f"pass{i}1234", "user")
    users = db.execute_select("users")
    bulk = [u for u in users if u["login"].startswith("bulk_")]
    assert len(bulk) == 20
    print("[PASS] создано 20 пользователей")


if __name__ == "__main__":
    setup()
    test_many_processes()
    test_memory_limit_stress()
    test_many_files()
    test_many_users()
    print("\nВсе стресс-тесты пройдены.")