
 3. Спецификация системных вызовов

Все системные вызовы реализованы в `syscalls.py`. Они вызываются
из оболочки и никогда — напрямую из пользовательского кода.

| Вызов             | Параметры                                | Возвращает | Назначение                         |
|-------------------|------------------------------------------|------------|------------------------------------|
| `sys_login`       | login, password, current_user            | bool       | Вход в систему                     |
| `sys_logout`      | current_user                             | bool       | Выход из системы                   |
| `sys_whoami`      | current_user                             | str        | Текущий пользователь               |
| `sys_create_file` | path, content, current_user              | int        | Создать файл, вернуть id           |
| `sys_read_file`   | path, current_user                       | str        | Прочитать файл                     |
| `sys_delete_file` | path, current_user, owner                | bool       | Удалить файл (с проверкой прав)    |
| `sys_list_files`  | path, current_user                       | list       | Список файлов по префиксу          |
| `sys_exec`        | name, current_user, memory_size          | int        | Запустить процесс, вернуть PID     |
| `sys_ps`          | current_user                             | list       | Список процессов                   |
| `sys_kill`        | pid, current_user                        | bool       | Завершить процесс                  |
| `sys_mem_alloc`   | size, current_user                       | int        | Выделить память                    |
| `sys_logs`        | limit, current_user                      | list       | Последние записи журнала           |
| `sys_shutdown`    | current_user                             | bool       | Завершить работу ОС                |

 4. Контракты трёх вызовов

Контракт функции — это её "обещание": что должно быть до вызова,
что будет после и какие побочные эффекты.

 4.1. sys_login

- **Предварительное условие:** пользователь с таким логином есть в таблице users.
- **Постусловие:** возвращено True, если пароль совпал с хэшем; иначе False.
- **Побочный эффект:** запись в `syscalls_log` со статусом check и OK/DENIED.

 4.2. sys_create_file

- **Предварительное условие:** пользователь авторизован.
- **Постусловие:** файл создан, возвращён его id. Если файл уже существует — вернуть -1.
- **Побочный эффект:** запись в таблицу files и запись в syscalls_log.

 4.3. sys_delete_file

- **Предварительное условие:** файл существует, у пользователя есть права.
- **Постусловие:** файл удалён, возвращено True. Иначе — False.
- **Побочный эффект:** удаление из таблицы files, запись в syscalls_log
  со статусом OK или DENIED.

 5. Структуры данных ядра

В Python структуры представлены словарями. Они описывают записи
в таблицах базы данных.

 process

```python
process = {
    'pid': 1,
    'name': 'shell',
    'state': 'running',       # ready | running | waiting
    'owner': 'admin',
    'memory_used': 120,
    'created_at': '2025-01-01 10:00:00'
}
file = {
    'id': 1,
    'path': '/home/test.txt',
    'content': 'hello',
    'owner': 'admin',
    'is_directory': 0,
    'created_at': '2025-01-01 10:00:00'
}
user = {
    'id': 1,
    'login': 'admin',
    'password_hash': 'abc123...',  # SHA-256, 64 символа
    'role': 'admin',               # admin | user | guest
    'created_at': '2025-01-01 10:00:00'
}
log = {
    'id': 1,
    'syscall_name': 'sys_login',
    'args': 'admin',
    'user': 'admin',
    'status': 'OK',                # check | OK | DENIED | EXISTS | NOT_FOUND
    'timestamp': '2025-01-01 10:00:00'
}
