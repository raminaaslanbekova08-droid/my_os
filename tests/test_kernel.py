"""Модульные тесты ядра."""

from src.kernel import Kernel


def test_pid_increments():
    k = Kernel()
    pid1 = k.allocate_pid()
    pid2 = k.allocate_pid()
    assert pid2 == pid1 + 1
    print(f"[PASS] PID увеличивается {pid1} -> {pid2}")


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
    print("[PASS] лимит памяти соблюдается")


def test_free_memory():
    k = Kernel()
    k.memory_used = 0
    k.allocate_memory(100)
    k.free_memory(100)
    assert k.memory_info()["used"] == 0
    print("[PASS] память освобождена")


def test_session_create():
    k = Kernel()
    sid = k.create_session("admin")
    assert sid > 0
    assert k.get_user() == "admin"
    print("[PASS] создание сессии")


if __name__ == "__main__":
    test_pid_increments()
    test_memory_allocate()
    test_memory_limit()
    test_free_memory()
    test_session_create()
    print("\nВсе тесты kernel.py пройдены.")