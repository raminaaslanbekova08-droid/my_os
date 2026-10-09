 Спецификации модулей StudyOS

Документ описывает каждый модуль ОС по единой структуре:
1. Назначение
2. Публичный интерфейс
3. Внутренние зависимости
4. Обработка ошибок
5. Побочные эффекты



 6. Модуль `db.py`

 Назначение

Слой работы с базой данных SQLite. Создаёт таблицы при первом запуске
и предоставляет универсальные функции CRUD всем остальным модулям.

 Публичный интерфейс

- `get_connection() -> sqlite3.Connection` — соединение с базой.
- `init_db() -> None` — создаёт таблицы, если их нет.
- `execute_insert(table: str, data: dict) -> int` — вставка, возвращает id.
- `execute_select(table: str, conditions: dict = None) -> list` — выборка.
- `execute_update(table: str, data: dict, conditions: dict) -> None` — обновление.
- `execute_delete(table: str, conditions: dict) -> None` — удаление.

 Внутренние зависимости

Не зависит от других модулей проекта. Использует стандартный `sqlite3`.

 Обработка ошибок

- `sqlite3.OperationalError` (база заблокирована) — повторная попытка через 100 мс.
- `sqlite3.IntegrityError` (нарушен UNIQUE) — вернуть `None`.
- Все остальные `sqlite3.Error` — логируются в stderr.

 Побочные эффекты

- Создание файла `db/os.sqlite` при первом запуске.
- Создание таблиц `users`, `processes`, `files`, `syscalls_log`, `memory_state`, `roles`.


 2. Модуль `syscalls.py`

 Назначение

Единый интерфейс между оболочкой и ядром. Каждая функция проверяет
аргументы, вызывает соответствующую логику и записывает вызов в журнал.

 Публичный интерфейс

- `log_syscall(name, args, user, status) -> None`
- `check_permission(current_user, action, target_owner) -> bool`
- `sys_login(login, password, current_user) -> bool`
- `sys_logout(current_user) -> bool`
- `sys_whoami(current_user) -> str`
- `sys_create_file(path, content, current_user) -> int`
- `sys_read_file(path, current_user) -> str`
- `sys_delete_file(path, current_user, owner) -> bool`
- `sys_list_files(path, current_user) -> list`
- `sys_exec(name, current_user, memory_size) -> int`
- `sys_ps(current_user) -> list`
- `sys_kill(pid, current_user) -> bool`
- `sys_mem_alloc(size, current_user) -> int`
- `sys_logs(limit, current_user) -> list`
- `sys_shutdown(current_user) -> bool`

 Внутренние зависимости

- `db.py` — для записи в `syscalls_log`.
- `auth.py` — для проверки прав (на следующих занятиях).
- `kernel.py` — для реальной логики (на следующих занятиях).

 Обработка ошибок

- Пользователь не авторизован → `sys_create_file` возвращает `-1`.
- Файл не найден → `sys_read_file` возвращает пустую строку.
- PID не существует → `sys_kill` возвращает `False`.
- Нет прав на удаление файла → `sys_delete_file` возвращает `False` и статус `DENIED`.
- Нет прав на завершение процесса → `sys_kill` возвращает `False` и статус `DENIED`.

 Побочные эффекты

Каждый вызов пишет строку в `syscalls_log` с полями:
`syscall_name`, `args`, `user`, `status`, `timestamp`.



 3. Модуль `kernel.py`

 Назначение

Хранит состояние системы: текущего пользователя, счётчик PID,
объём используемой памяти и её лимит. Делегирует работу подсистемам.

 Публичный интерфейс

- `Kernel()` — конструктор.
- `set_user(login) -> None`
- `get_user() -> str`
- `allocate_pid() -> int`
- `allocate_memory(size) -> bool`
- `free_memory(size) -> None`
- `memory_info() -> dict`
- `save_memory_state() -> None`
- `load_memory_state() -> None`
- `kernel_instance` — глобальный экземпляр.

 Внутренние зависимости

- `db.py` — для сохранения состояния памяти.

 Обработка ошибок

- Превышение лимита памяти → `allocate_memory` возвращает `False`.

 Побочные эффекты

- Обновление таблицы `memory_state` при выделении/освобождении памяти.



 4. Модуль `scheduler.py`

 Назначение

Управление процессами: создание, вывод списка, завершение, планирование.

 Публичный интерфейс

- `create_process(name, owner, memory_size) -> int`
- `list_processes() -> list`
- `get_process(pid) -> dict | None`
- `terminate_process(pid) -> bool`
- `schedule_round_robin() -> dict | None`
- `process_count() -> int`

 Внутренние зависимости

- `db.py` — таблица `processes`.
- `kernel.py` — выделение памяти и PID.

 Обработка ошибок

- Не хватает памяти → `create_process` возвращает `-1`.
- Процесс не найден → `terminate_process` возвращает `False`.

 Побочные эффекты

- Запись/удаление строк в таблице `processes`.
- Изменение состояния процессов (`ready`/`running`).



 5. Модуль `memory.py`

 Назначение

Обёртка над методами ядра для работы с памятью.

 Публичный интерфейс

- `alloc(size) -> bool`
- `free(size) -> None`
- `info() -> dict`

 Внутренние зависимости

- `kernel.py` — `kernel_instance`.

 Обработка ошибок

- Превышение лимита → `alloc` возвращает `False`.

 Побочные эффекты

- Обновление состояния памяти в БД (через ядро).



 6. Модуль `fs.py`

 Назначение

Файловая система. Создание, чтение, запись, удаление, список файлов.
Работает с таблицей `files` базы данных.

 Публичный интерфейс

- `create_file(path, content, owner) -> int`
- `read_file(path) -> str`
- `write_file(path, content) -> bool`
- `delete_file(path) -> bool`
- `list_files(prefix) -> list`
- `get_owner(path) -> str | None`
- `get_file_info(path) -> dict | None`
- `mkdir(path, owner) -> int`
- `rmdir(path, owner) -> bool`
- `rename_file(old, new, owner) -> bool`
- `copy_file(src, dst, owner) -> bool`
- `move_file(src, dst, owner) -> bool`
- `tree(path) -> str`

 Внутренние зависимости

- `db.py` — таблица `files`.

 Обработка ошибок

- Файл уже существует → `create_file` возвращает `-1`.
- Файл не найден → `read_file` возвращает пустую строку.
- Нет прав → `delete_file` возвращает `False`.

 Побочные эффекты

- Создание / изменение / удаление строк в `files`.
- Запись в `syscalls_log` через `syscalls.py`.



 7. Модуль `auth.py`

 Назначение

Аутентификация (вход) и авторизация (проверка прав).

 Публичный интерфейс

- `hash_password(password) -> str` — SHA-256.
- `register_user(login, password, role) -> int | None`
- `authenticate(login, password) -> dict | None`
- `check_permission(current_user, action, target_owner) -> bool`
- `change_password(login, old, new) -> bool`

 Внутренние зависимости

- `db.py` — таблица `users`.
- `hashlib` — стандартная библиотека.

 Обработка ошибок

- Логин занят → `register_user` возвращает `None`.
- Неверный пароль → `authenticate` возвращает `None`.
- Пароль короче 4 символов → `register_user` возвращает `None`.

 Побочные эффекты

- Добавление/изменение строк в таблице `users`.
- При успешном входе ядро сохраняет текущего пользователя.



 1. Модуль `shell.py`
 Назначение

Командная оболочка: читает команды пользователя, вызывает системные
вызовы, выводит результат.

 Публичный интерфейс

- `main() -> None`

Команды: `help`, `echo`, `whoami`, `login`, `logout`, `create`, `cat`,
`ls`, `mkdir`, `rmdir`, `cd`, `pwd`, `tree`, `copy`, `move`, `run`, `ps`,
`kill`, `mem`, `logs`, `exit`.

 Внутренние зависимости

- `syscalls.py` — все вызовы ядра.
- `kernel.py` — отображение состояния памяти.

 Обработка ошибок

- Пустой ввод — игнорируется.
- Неизвестная команда — выводится сообщение.

 Побочные эффекты

- Вывод в stdout.
- Через системные вызовы — изменение состояния системы.



 Матрица трассируемости требований

| Требование                                    | Модуль                   | Тест              |
|-----------------------------------------------|--------------------------|-------------------|
| NFR-1: Время обработки syscall ≤ 50 мс        | `syscalls.py`            | `TC-01`           |
| NFR-2: ОС выдерживает 10 одновременных процессов | `scheduler.py`        | `TC-02`           |
| NFR-3: Ошибка в процессе не роняет ядро       | `kernel.py`              | `TC-03`           |
| NFR-4: Пароли хранятся как SHA-256            | `auth.py`                | `TC-04`           |
| NFR-5: User не может удалить файл Admin       | `syscalls.py`, `auth.py` | `TC-02`           |
| NFR-6: Модуль ≤ 300 строк                     | все модули               | `TC-03`           |
| NFR-7: Все системные вызовы логируются        | `syscalls.py`, `db.py`   | `TC-05`           |
| NFR-8: ОС работает без внешних СУБД           | все модули               | `TC-08`           |

 Пояснения по требованиям

**NFR-4: Пароли хранятся как SHA-256.** Модуль `auth.py` при регистрации
вычисляет хэш через `hashlib.sha256` и сохраняет в поле `password_hash`.

**NFR-5: User не может удалить файл Admin.** `syscalls.sys_delete_file`
перед удалением вызывает `check_permission`. Если владелец файла не
совпадает с пользователем и он не администратор — возвращается `False`
и в лог пишется `DENIED`.

**NFR-7: Все системные вызовы логируются.** Каждая функция в
`syscalls.py` вызывает `log_syscall(...)` минимум дважды.


 Тест-кейсы

 TC-01: Проверка времени обработки syscall (NFR-1)

**Шаги:**
1. Запустить интерпретатор Python.
2. Импортировать `sys_create_file` из `src.syscalls`.
3. Замерить время через `time.perf_counter()` до и после вызова.
4. Повторить 100 раз.
5. Вычислить среднее время.

**Ожидаемый результат:** среднее время ≤ 50 мс.
**Фактический результат:** ---
**Статус:** ---

 TC-02: Проверка разграничения прав (NFR-5)

**Шаги:**
1. Авторизоваться как guest.
2. Создать файл от имени admin.
3. От имени guest вызвать `sys_delete_file` для этого файла.
4. Проверить возвращаемое значение.

**Ожидаемый результат:** возвращено `False`.
**Фактический результат:** пройдено.
**Статус:** PASS

 TC-03: Проверка размера модулей (NFR-6)

**Шаги:**
1. Открыть терминал в корне проекта.
2. Выполнить: `wc -l src/*.py`.
3. Проверить, что ни один файл не превышает 300 строк.

**Ожидаемый результат:** все файлы ≤ 300 строк.
**Фактический результат:** ---
**Статус:** ---

 TC-04: Проверка хэширования пароля (NFR-4)

**Шаги:**
1. Создать файл `tests/test_auth.py`.
2. Запустить: `python -m tests.test_auth`.
3. Убедиться, что длина хэша равна 64.

**Ожидаемый результат:** `len(hash) == 64`.
**Фактический результат:** ---
**Статус:** ---

 TC-05: Проверка логирования отказов (NFR-7)

**Шаги:**
1. Выполнить `sys_delete_file("/x.txt", "guest", owner="admin")`.
2. Открыть `db/os.sqlite` через SQLite Viewer.
3. В таблице `syscalls_log` найти запись `sys_delete_file` со статусом `DENIED`.

**Ожидаемый результат:** запись со статусом `DENIED` присутствует.
**Фактический результат:** ---
**Статус:** ---



 Итоги дня 3

 Что сделано

- Составлены спецификации для восьми модулей.
- Построена матрица трассируемости для восьми требований.
- Разработаны пять тест-кейсов.
- Реализована функция `check_permission`.
- Внедрена проверка прав в `sys_delete_file` и `sys_kill`.
- Написаны автоматические тесты в `tests/test_permissions.py`.
- Построена диаграмма последовательности `03_sequence_permissions.png`.