
 3. Спецификация системных вызовов

| Вызов | Сигнатура | Возвращает |
|-------|-----------|------------|
| sys_login | (login, password, current_user) | bool |
| sys_logout | (current_user) | bool |
| sys_whoami | (current_user) | str |
| sys_create_file | (path, content, current_user) | int |
| sys_read_file | (path, current_user) | str |
| sys_delete_file | (path, current_user) | bool |
| sys_list_files | (path, current_user) | list |
| sys_exec | (name, current_user) | int |
| sys_ps | (current_user) | list |
| sys_kill | (pid, current_user) | bool |
| sys_mem_alloc | (size, current_user) | int |
| sys_logs | (limit, current_user) | list |
| sys_shutdown | (current_user) | bool |

 4. Контракты функций

 sys_login
- **Предусловие:** пользователь существует в БД
- **Постусловие:** возвращено True или False
- **Побочный эффект:** запись в syscalls_log

 sys_create_file
- **Предусловие:** пользователь авторизован
- **Постусловие:** файл создан, возвращён его id
- **Побочный эффект:** запись в syscalls_log

 sys_delete_file
- **Предусловие:** пользователь авторизован, файл существует
- **Постусловие:** файл удалён, возвращено True
- **Побочный эффект:** запись в syscalls_log

 5. Структуры данных

```python
process = {
    'pid': 1,
    'name': 'shell',
    'state': 'running',
    'owner': 'admin',
    'memory': 120,
    'created_at': '2025-01-01 10:00:00'
}

file = {
    'id': 1,
    'path': '/home/test.txt',
    'content': 'hello',
    'owner': 'admin',
    'created_at': '2025-01-01 10:00:00'
}

user = {
    'id': 1,
    'login': 'admin',
    'password_hash': 'abc123...',
    'role': 'admin'
}

log = {
    'id': 1,
    'syscall_name': 'sys_login',
    'args': 'admin',
    'user': 'admin',
    'status': 'OK',
    'timestamp': '2025-01-01 10:00:00'
}