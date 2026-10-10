"""Тесты планировщика."""

from src import scheduler, db
from src.kernel import kernel_instance


def setup():
    """Очищаем процессы и сбрасываем память."""
    for p in db.execute_select("processes"):
        db.execute_delete("processes", {"pid": p["pid"]})
    kernel_instance.reset()


def test_create_process():
    pid = scheduler.create_process("test_app", "admin", 10)
    assert pid > 0
    print(f"[PASS] процесс создан, PID={pid}")


def test_memory_limit():
    before = kernel_instance.memory_used
    pid = scheduler.create_process("huge", "admin", 5000)
    assert pid == -1
    assert kernel_instance.memory_used == before
    print("[PASS] переполнение памяти отклонено")


def test_terminate_frees_memory():
    pid = scheduler.create_process("temp", "admin", 50)
    used_after_create = kernel_instance.memory_used
    scheduler.terminate_process(pid)
    assert kernel_instance.memory_used == used_after_create - 50
    print("[PASS] память освобождена при завершении")


def test_get_process():
    pid = scheduler.create_process("lookup", "admin", 5)
    p = scheduler.get_process(pid)
    assert p is not None and p["name"] == "lookup"
    print("[PASS] поиск процесса по PID")


def test_terminate_nonexistent():
    assert scheduler.terminate_process(99999) is False
    print("[PASS] завершение несуществующего процесса")


def test_round_robin():
    scheduler.create_process("rr1", "admin", 5)
    scheduler.create_process("rr2", "admin", 5)
    running = scheduler.schedule_round_robin()
    assert running is not None and running["state"] == "running"
    print("[PASS] Round Robin выбирает процесс")


if __name__ == "__main__":
    setup()
    test_create_process()
    test_memory_limit()
    test_terminate_frees_memory()
    test_get_process()
    test_terminate_nonexistent()
    test_round_robin()
    print("\nВсе тесты планировщика пройдены.")