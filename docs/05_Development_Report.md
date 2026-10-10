 Отчёт по дню 5

 Что сделано

- Создан `src/fs.py` с функциями `create_file`, `read_file`,
  `write_file`, `delete_file`, `list_files`, `get_owner`, `get_file_info`,
  а также `mkdir`, `rmdir`, `rename_file`, `copy_file`, `move_file`, `tree`.
- Создан `src/scheduler.py` с функциями `create_process`, `list_processes`,
  `get_process`, `terminate_process`, `schedule_round_robin`, `process_count`.
- Обновлён `syscalls.py`: файловые и процессные вызовы используют
  реальные модули `fs` и `scheduler`.
- Обновлён `shell.py`: команды `cat`, `run`, `kill`, `ls`, `create`.
- Написаны `tests/test_fs.py` (6 тестов) и `tests/test_scheduler.py` (6 тестов).
- Расширена спецификация в `docs/03_Module_Specifications.md`.

 Проверки

- Сквозной сценарий: вход, создание файлов, чтение, запуск процессов,
  kill, mem.
- Записи в `syscalls_log` со статусами `check`, `OK`, `EXISTS`, `DENIED`,
  `NOT_FOUND`.
- Память освобождается при завершении процесса.
- Дубликат пути возвращает -1.

 Замечания

- Round Robin упрощён: выбирает первый процесс из очереди.
- При создании файла с существующим путём возвращается -1 и статус EXISTS.

 