"""Файловая система на SQLite."""
from src import db


def create_file(path, content, owner):
    """Создаёт файл. Возвращает id или -1."""
    existing = db.execute_select('files', {'path': path})
    if existing:
        return -1
    file_id = db.execute_insert('files', {
        'path': path,
        'content': content,
        'owner': owner
    })
    return file_id


def read_file(path):
    """Возвращает содержимое файла или пустую строку."""
    files = db.execute_select('files', {'path': path})
    if not files:
        return ""
    return files[0]['content']


def write_file(path, content):
    """Обновляет содержимое файла."""
    db.execute_update('files', {'content': content}, {'path': path})
    return True


def delete_file(path):
    """Удаляет файл."""
    db.execute_delete('files', {'path': path})
    return True


def list_files(prefix=""):
    """Возвращает список путей, начинающихся с префикса."""
    all_files = db.execute_select('files')
    return [f['path'] for f in all_files if f['path'].startswith(prefix)]


def get_owner(path):
    """Возвращает владельца файла или None."""
    files = db.execute_select('files', {'path': path})
    if not files:
        return None
    return files[0]['owner']


def get_file_info(path):
    """Возвращает полную информацию о файле."""
    files = db.execute_select('files', {'path': path})
    if not files:
        return None
    return files[0]