"""Модульные тесты ядра."""

from src.kernel import Kernel


def test_pid_increments():
    k = Kernel()
    pid1 = k.allocate_pid()
    pid2 = k.allocate_pid()
    assert pid2 == pid1 + 1
    print(f"[PASS] TC-05: PID увеличивается {pid1} -> {pid2}")


def test_memory_allocate():
    k = Kernel()
    k.memory_used = 0
    assert k.allocate_memory(100) is True
    assert k.memory_info()["used"] == 100
    print("[PASS] выделение памяти")


def test_memory_limit():
    k = Kernel()
    k.memory_used = 0
    assert k.allocate_memory(5000) is False
    print("[PASS] TC-06: лимит памяти соблюдается")


def test_free_memory():
    k = Kernel()
    k.memory_used = 0
    k.allocate_memory(100)
    k.free_memory(100)
    assert k.memory_info()["used"] == 0
    print("[PASS] TC-07: память освобождена")


def test_free_more_than_used():
    k = Kernel()
    k.memory_used = 0
    k.allocate_memory(50)
    k.free_memory(100)
    assert k.memory_info()["used"] == 0
    print("[PASS] освобождение большего объёма не даёт отрицательного значения")


def test_session_create():
    k = Kernel()
    sid = k.create_session("admin")
    assert sid > 0
    assert k.get_user() == "admin"
    print("[PASS] создание сессии")


def test_session_switch():
    k = Kernel()
    s1 = k.create_session("admin")
    k.create_session("user")
    assert k.switch_session(s1) is True
    assert k.get_user() == "admin"
    print("[PASS] переключение сессий")


def test_session_list():
    k = Kernel()
    k.create_session("admin")
    k.create_session("user")
    assert len(k.list_sessions()) == 2
    print("[PASS] список сессий")


if __name__ == "__main__":
    test_pid_increments()
    test_memory_allocate()
    test_memory_limit()
    test_free_memory()
    test_free_more_than_used()
    test_session_create()
    test_session_switch()
    test_session_list()
    print("\nВсе тесты kernel.py пройдены.")