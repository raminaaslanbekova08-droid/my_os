 Функциональные тесты

 Модуль fs.py
Функции: create_file, read_file, write_file, delete_file,
list_files, get_owner, get_file_info.

 FT-01: create_file создаёт файл
Ожидаемый результат: id > 0, запись в files.

 FT-02: create_file отклоняет дубликат
Ожидаемый результат: -1.

 FT-03: read_file возвращает содержимое
Ожидаемый результат: 'hello'.

 FT-04: read_file для несуществующего
Ожидаемый результат: ''.

 FT-05: write_file обновляет
Ожидаемый результат: 'new'.

 FT-06: delete_file удаляет
Ожидаемый результат: ''.

 FT-07: list_files по префиксу
Ожидаемый результат: список с обоими файлами.

 FT-08: get_owner возвращает владельца
Ожидаемый результат: 'admin'.

 FT-09: get_owner для несуществующего
Ожидаемый результат: None.

 FT-10: get_file_info
Ожидаемый результат: словарь с полями.

 Модуль scheduler.py

 FT-10..FT-18
Аналогично для create_process, memory_overflow, list_processes,
get_process, get_missing, terminate_frees_memory, terminate_missing,
round_robin, process_count.