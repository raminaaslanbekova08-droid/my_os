"""Планировщик процессов."""

from src import db
from src.kernel import kernel_instance


def create_process(name, owner, memory_size=10):
    """Создаёт процесс. Возвращает pid или -1."""
    if not kernel_instance.allocate_memory(memory_size):
        return -1
    pid = kernel_instance.allocate_pid()
    db.execute_insert("processes", {
        "pid": pid,
        "name": name,
        "state": "ready",
        "owner": owner,
        "memory_used": memory_size,
    })
    return pid


def list_processes():
    return db.execute_select("processes")


def get_process(pid):
    procs = db.execute_select("processes", {"pid": pid})
    return procs[0] if procs else None


def terminate_process(pid):
    process = get_process(pid)
    if not process:
        return False
    kernel_instance.free_memory(process["memory_used"])
    db.execute_delete("processes", {"pid": pid})
    return True


def schedule_round_robin():
    """Round Robin: первый в очереди — running, остальные ready."""
    processes = db.execute_select("processes")
    if not processes:
        return None
    for p in processes:
        db.execute_update("processes", {"state": "ready"}, {"pid": p["pid"]})
    first = processes[0]
    db.execute_update("processes", {"state": "running"}, {"pid": first["pid"]})
    return get_process(first["pid"])


def process_count():
    return len(list_processes())