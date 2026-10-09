"""Планировщик процессов."""
from src import db
from src.kernel import kernel_instance


def create_process(name, owner, memory_size=10):
    """Создаёт процесс. Возвращает pid или -1."""
    if not kernel_instance.allocate_memory(memory_size):
        return -1
    pid = kernel_instance.allocate_pid()
    db.execute_insert('processes', {
        'pid': pid,
        'name': name,
        'state': 'ready',
        'owner': owner,
        'memory_used': memory_size
    })
    return pid


def list_processes():
    """Возвращает список всех процессов."""
    return db.execute_select('processes')


def get_process(pid):
    """Возвращает процесс по pid или None."""
    processes = db.execute_select('processes', {'pid': pid})
    if not processes:
        return None
    return processes[0]


def terminate_process(pid):
    """Завершает процесс. Освобождает память."""
    process = get_process(pid)
    if not process:
        return False
    kernel_instance.free_memory(process['memory_used'])
    db.execute_delete('processes', {'pid': pid})
    return True


def schedule_round_robin():
    """Выбирает следующий процесс по Round Robin."""
    processes = db.execute_select('processes')
    if not processes:
        return None
    for p in processes:
        db.execute_update('processes', {'state': 'ready'}, {'pid': p['pid']})
    first = processes[0]
    db.execute_update('processes', {'state': 'running'}, {'pid': first['pid']})
    return get_process(first['pid'])


def process_count():
    """Возвращает количество процессов."""
    return len(list_processes())