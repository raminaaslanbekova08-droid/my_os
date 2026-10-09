"""Файловая система на SQLite."""

import os

from src import db


def exists(path):
    return len(db.execute_select("files", {"path": path})) > 0


def is_directory(path):
    files = db.execute_select("files", {"path": path})
    return bool(files) and files[0]["is_directory"] == 1


def _resolve_parent_id(parent_path):
    if not parent_path or parent_path == "/":
        return None
    parents = db.execute_select("files", {"path": parent_path})
    if not parents:
        return -1
    return parents[0]["id"]


def create_file(path, content, owner):
    """Создаёт файл. Возвращает id или -1, если файл уже существует."""
    if exists(path):
        return -1
    parent_path = os.path.dirname(path)
    parent_id = _resolve_parent_id(parent_path)
    if parent_id == -1:
        return -1
    return db.execute_insert("files", {
        "path": path,
        "content": content,
        "owner": owner,
        "is_directory": 0,
        "parent_id": parent_id,
    })


def read_file(path):
    """Возвращает содержимое или пустую строку."""
    files = db.execute_select("files", {"path": path})
    if not files or files[0]["is_directory"]:
        return ""
    return files[0]["content"] or ""


def write_file(path, content):
    """Обновляет содержимое файла."""
    if not exists(path):
        return False
    db.execute_update("files", {"content": content}, {"path": path})
    return True


def delete_file(path):
    """Удаляет файл. Возвращает True."""
    if not exists(path):
        return False
    db.execute_delete("files", {"path": path})
    return True


def list_files(prefix=""):
    """Список путей, начинающихся с префикса."""
    all_files = db.execute_select("files")
    return [f["path"] for f in all_files if f["path"].startswith(prefix)]


def get_owner(path):
    """Возвращает владельца или None."""
    files = db.execute_select("files", {"path": path})
    return files[0]["owner"] if files else None


def get_file_info(path):
    """Полная информация о файле."""
    files = db.execute_select("files", {"path": path})
    return files[0] if files else None


def mkdir(path, owner):
    """Создаёт каталог. Возвращает id или -1."""
    if exists(path):
        return -1
    parent_path = os.path.dirname(path)
    parent_id = _resolve_parent_id(parent_path)
    if parent_id == -1:
        return -1
    return db.execute_insert("files", {
        "path": path,
        "content": None,
        "owner": owner,
        "is_directory": 1,
        "parent_id": parent_id,
    })


def rmdir(path, owner):
    """Рекурсивно удаляет каталог и всё его содержимое."""
    if not exists(path):
        return False
    all_files = db.execute_select("files")
    for f in all_files:
        if f["path"] == path or f["path"].startswith(path + "/"):
            db.execute_delete("files", {"id": f["id"]})
    return True


def rename_file(old_path, new_path, owner):
    """Переименовывает файл."""
    if not exists(old_path) or exists(new_path):
        return False
    db.execute_update("files", {"path": new_path}, {"path": old_path})
    return True


def copy_file(src, dst, owner):
    """Копирует файл."""
    if not exists(src) or exists(dst):
        return False
    info = get_file_info(src)
    if info["is_directory"]:
        return False
    return create_file(dst, info["content"], owner) != -1


def move_file(src, dst, owner):
    """Перемещает файл."""
    if not exists(src) or exists(dst):
        return False
    db.execute_update("files", {"path": dst}, {"path": src})
    return True


def tree(path="/"):
    """Возвращает текстовое дерево каталогов."""
    all_files = db.execute_select("files")
    lines = []

    def walk(parent_id, indent):
        for f in all_files:
            if f["parent_id"] == parent_id:
                name = os.path.basename(f["path"]) or f["path"]
                suffix = "/" if f["is_directory"] else ""
                lines.append("  " * indent + name + suffix)
                if f["is_directory"]:
                    walk(f["id"], indent + 1)

    root = next((f for f in all_files if f["path"] == path), None)
    if root:
        lines.append(os.path.basename(root["path"]) + "/")
        walk(root["id"], 1)
    else:
        walk(None, 0)
    return "\n".join(lines)