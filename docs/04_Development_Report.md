 Отчёт по дню 4

 Что сделано

- Расширен `db.py`: добавлены `execute_insert`, `execute_select`,
  `execute_update`, `execute_delete`, таблица `memory_state`.
- Создан `kernel.py` с классом `Kernel` и шестью методами.
- Создан `auth.py` с функциями `hash_password`, `register_user`,
  `authenticate`, `check_permission`, `change_password`.
- Обновлён `syscalls.py`: `sys_login`, `sys_whoami`, `sys_delete_file`,
  `sys_kill` используют реальные модули.
- Обновлён `shell.py`: команды `login`, `mem`, `delete`, `logs` работают.
- Написаны тесты `test_kernel.py` и `test_auth.py`.

 Проверки

- Записи в `syscalls_log` со статусами `check`, `OK`, `DENIED`.
- Пароль в базе хранится в виде хэша длиной 64 символа.
- Права разграничены: admin может всё, user — нет.

 Замечания

- Пустой пароль допускается. В следующих итерациях добавить валидацию.

 Скриншоты

![Отладка](04_debug_screenshot.png)

![Таблица syscalls_log](04_syscalls_log.png)