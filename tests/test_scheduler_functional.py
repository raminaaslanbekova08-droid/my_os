"""Функциональные тесты планировщика."""

from src import scheduler, db
from src.kernel import kernel_instance


def setup():
    for p in db.execute_select("processes"):
        db.execute_delete("processes", {"pid": p["pid"]})
    kernel_instance.reset()


def test_create_process():
    pid = scheduler.create_process("ft_app", "admin", 10)
    assert pid > 0
    print("[PASS] FT-10: создание процесса")


def test_memory_overflow():
    pid = scheduler.create_process("huge", "admin", 5000)
    assert pid == -1
    print("[PASS] FT-11: отклонение при переполнении")


def test_list_processes():
    scheduler.create_process("p1", "admin", 5)
    scheduler.create_process("p2", "admin", 5)
    assert len(scheduler.list_processes()) >= 2
    print("[PASS] FT-12: список процессов")


def test_get_process():
    pid = scheduler.create_process("lookup", "admin", 5)
    p = scheduler.get_process(pid)
    assert p and p["name"] == "lookup"
    print("[PASS] FT-13: поиск по PID")


def test_get_missing():
    assert scheduler.get_process(99999) is None
    print("[PASS] FT-14: None для несуществующего PID")


def test_terminate_frees_memory():
    pid = scheduler.create_process("temp", "admin", 50)
    used = kernel_instance.memory_used
    scheduler.terminate_process(pid)
    assert kernel_instance.memory_used == used - 50
    print("[PASS] FT-15: завершение освобождает память")


def test_terminate_missing():
    assert scheduler.terminate_process(99999) is False
    print("[PASS] FT-16: False для несуществующего")


def test_round_robin():
    scheduler.create_process("rr1", "admin", 5)
    scheduler.create_process("rr2", "admin", 5)
    p = scheduler.schedule_round_robin()
    assert p and p["state"] == "running"
    print("[PASS] FT-17: Round Robin")


def test_process_count():
    scheduler.create_process("c1", "admin", 5)
    assert scheduler.process_count() >= 1
    print("[PASS] FT-18: подсчёт процессов")


if __name__ == "__main__":
    setup()
    test_create_process()
    test_memory_overflow()
    test_list_processes()
    test_get_process()
    test_get_missing()
    test_terminate_frees_memory()
    test_terminate_missing()
    test_round_robin()
    test_process_count()
    print("\nВсе функциональные тесты планировщика пройдены.")