 Отчёт о разработке за дни 4–6

 Что сделано

Реализованы 9 модулей: db.py, kernel.py, auth.py, fs.py, scheduler.py,
logger.py, syscalls.py, shell.py, config.py.

Реализованы все системные вызовы: sys_login, sys_logout, sys_whoami,
sys_create_file, sys_read_file, sys_delete_file, sys_list_files,
sys_exec, sys_ps, sys_kill, sys_mem_alloc, sys_logs, sys_shutdown.

Тесты: test_kernel.py, test_auth.py, test_permissions.py, test_fs.py,
test_scheduler.py, test_integration.py.

 Ошибки и исправления

1. sys_delete_file не проверял владельца — добавлен вызов fs.get_owner.
2. syscalls.py использовал заглушки — подключены fs и scheduler.

 Покрытие

- auth.py — 4 теста
- fs.py — 6 тестов
- scheduler.py — 6 тестов
- kernel.py — 5 тестов
- syscalls.py — 7 интеграционных
- Всего: 28 тестов, все проходят.

 Выполненные NFR

NFR-1..NFR-8 — PASS.

 Дальше

Полное тестирование (дни 7–9).