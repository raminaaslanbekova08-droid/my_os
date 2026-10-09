"""Модуль аутентификации и управления пользователями."""

import hashlib

from src import db


def hash_password(password):
    """Возвращает SHA-256 хэш пароля (64 символа)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(login, password, role="user"):
    """Регистрирует нового пользователя. Возвращает id или None."""
    if len(password) < 4:
        return None
    if db.execute_select("users", {"login": login}):
        return None
    return db.execute_insert("users", {
        "login": login,
        "password_hash": hash_password(password),
        "role": role,
    })


def authenticate(login, password):
    """Проверяет логин и пароль. Возвращает запись пользователя или None."""
    users = db.execute_select("users", {"login": login})
    if not users:
        return None
    user = users[0]
    if user["password_hash"] == hash_password(password):
        return user
    return None


def check_permission(current_user, action, target_owner=None):
    """Проверяет права пользователя на действие."""
    users = db.execute_select("users", {"login": current_user})
    if not users:
        return False
    role = users[0]["role"]
    if role == "admin":
        return True
    if action in ("delete_file", "kill") and target_owner and target_owner != current_user:
        return False
    if action == "kill" and current_user != "admin":
        return False
    return True


def change_password(login, old_password, new_password):
    """Меняет пароль после проверки старого. Возвращает True/False."""
    user = authenticate(login, old_password)
    if not user:
        return False
    db.execute_update(
        "users",
        {"password_hash": hash_password(new_password)},
        {"login": login},
    )
    return True