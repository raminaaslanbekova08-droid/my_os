"""Ядро учебной операционной системы."""
from src.config import MEMORY_LIMIT
from src import db


class Kernel:
    """Класс ядра — хранит состояние системы."""
    
    def __init__(self):
        self.current_user = "guest"
        self.process_counter = 0
        self.memory_used = 0
        self.memory_limit = MEMORY_LIMIT
        self.sync_pid_counter()
    
    def sync_pid_counter(self):
        """Синхронизирует счётчик PID с базой данных."""
        try:
            procs = db.execute_select('processes')
            if procs:
                max_pid = max(p['pid'] for p in procs)
                self.process_counter = max_pid
            else:
                self.process_counter = 0
        except Exception:
            self.process_counter = 0
    
    def set_user(self, login):
        """Устанавливает текущего пользователя."""
        self.current_user = login
    
    def get_user(self):
        """Возвращает текущего пользователя."""
        return self.current_user
    
    def allocate_pid(self):
        """Выделяет новый PID."""
        self.process_counter += 1
        return self.process_counter
    
    def allocate_memory(self, size):
        """Выделяет память. Возвращает True или False."""
        if self.memory_used + size > self.memory_limit:
            return False
        self.memory_used += size
        self.save_memory_state()
        return True
    
    def free_memory(self, size):
        """Освобождает память."""
        self.memory_used = max(0, self.memory_used - size)
        self.save_memory_state()
        return True
    
    def memory_info(self):
        """Возвращает информацию о памяти."""
        return {
            'used': self.memory_used,
            'limit': self.memory_limit,
            'free': self.memory_limit - self.memory_used
        }
    
    def save_memory_state(self):
        """Сохраняет состояние памяти в БД."""
        db.execute_delete('memory_state')
        db.execute_insert('memory_state', {
            'used': self.memory_used,
            'mem_limit': self.memory_limit
        })
    
    def load_memory_state(self):
        """Загружает состояние памяти из БД."""
        states = db.execute_select('memory_state')
        if states:
            self.memory_used = states[0]['used']
            self.memory_limit = states[0]['mem_limit']


kernel_instance = Kernel()