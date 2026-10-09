"""Ядро учебной операционной системы."""

from src import db


class Kernel:
    """Ядро системы: пользователь, PID, память, сессии."""

    def __init__(self):
        self.current_user = "guest"
        self.process_counter = 0
        self.memory_used = 0
        self.memory_limit = 1024
        self.sessions = []
        self.load_memory_state()
        procs = db.execute_select("processes")
        if procs:
            self.process_counter = max(p["pid"] for p in procs)

    def set_user(self, login):
        """Устанавливает текущего пользователя."""
        self.current_user = login

    def get_user(self):
        """Возвращает текущего пользователя."""
        return self.current_user

    def allocate_pid(self):
        """Выдаёт следующий свободный PID."""
        self.process_counter += 1
        return self.process_counter

    def allocate_memory(self, size):
        """Выделяет память. False — если превышен лимит."""
        if self.memory_used + size > self.memory_limit:
            return False
        self.memory_used += size
        self.save_memory_state()
        return True

    def free_memory(self, size):
        """Освобождает память (не ниже 0)."""
        self.memory_used = max(0, self.memory_used - size)
        self.save_memory_state()

    def memory_info(self):
        """Возвращает состояние памяти."""
        return {
            "used": self.memory_used,
            "limit": self.memory_limit,
            "free": self.memory_limit - self.memory_used,
        }

    def save_memory_state(self):
        """Сохраняет состояние памяти в БД."""
        db.execute_delete("memory_state", {})
        db.execute_insert("memory_state", {
            "used": self.memory_used,
            "limit_value": self.memory_limit,
        })

    def load_memory_state(self):
        """Загружает состояние памяти из БД."""
        states = db.execute_select("memory_state")
        if states:
            self.memory_used = states[0]["used"]
            self.memory_limit = states[0]["limit_value"]

    def create_session(self, login):
        """Создаёт сессию и возвращает её id."""
        sid = len(self.sessions) + 1
        self.sessions.append({"id": sid, "login": login})
        self.set_user(login)
        return sid

    def switch_session(self, sid):
        """Переключает сессию по id."""
        for s in self.sessions:
            if s["id"] == sid:
                self.set_user(s["login"])
                return True
        return False

    def list_sessions(self):
        """Возвращает список сессий."""
        return self.sessions

    def reset(self):
        """Сбрасывает пользователя и память."""
        self.current_user = "guest"
        self.memory_used = 0
        self.save_memory_state()


kernel_instance = Kernel()