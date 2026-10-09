"""Командная оболочка StudyOS."""
from src.syscalls import (
    sys_login, sys_logout, sys_whoami,
    sys_create_file, sys_read_file, sys_delete_file, sys_list_files,
    sys_exec, sys_ps, sys_kill, sys_logs
)
from src.kernel import kernel_instance

BANNER = """
========================================
  StudyOS v0.5 - учебная ОС
========================================
"""


def print_help():
    """Выводит справку."""
    print("""
Доступные команды:
  help    - справка
  whoami  - текущий пользователь
  login   - вход в систему
  logout  - выход
  create  - создать файл
  cat     - прочитать файл
  ls      - список файлов
  delete  - удалить файл
  run     - запустить процесс
  ps      - список процессов
  kill    - завершить процесс
  mem     - состояние памяти
  exit    - выход
""")


def main():
    """Главный цикл оболочки."""
    print(BANNER)
    current_user = "guest"
    
    while True:
        try:
            cmd = input(f"{current_user}@studyos:~$ ").strip()
        except EOFError:
            break
        
        if not cmd:
            continue
        
        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        if command == "help":
            print_help()
        elif command == "whoami":
            print(sys_whoami(current_user))
        elif command == "login":
            login = input("Логин: ")
            password = input("Пароль: ")
            if sys_login(login, password, current_user):
                current_user = login
                print(f"Вы вошли как {login}")
            else:
                print("Ошибка входа")
        elif command == "logout":
            sys_logout(current_user)
            current_user = "guest"
            print("Вы вышли из системы")
        elif command == "create":
            path = input("Путь: ")
            content = input("Содержимое: ")
            fid = sys_create_file(path, content, current_user)
            if fid == -1:
                print("Файл с таким путём уже существует")
            else:
                print(f"Создан файл с id={fid}")
        elif command == "cat":
            if not arg:
                print("Укажите путь к файлу")
            else:
                content = sys_read_file(arg, current_user)
                if content:
                    print(content)
                else:
                    print("(файл пуст или не существует)")
        elif command == "ls":
            files = sys_list_files(arg or "/", current_user)
            if not files:
                print("(Нет файлов)")
            else:
                for f in files:
                    print(f"  {f}")
        elif command == "delete":
            if not arg:
                print("Укажите путь к файлу")
            else:
                if sys_delete_file(arg, current_user):
                    print("Файл удалён")
                else:
                    print("Не удалось удалить файл")
        elif command == "run":
            if not arg:
                print("Укажите имя программы")
            else:
                pid = sys_exec(arg, current_user)
                if pid == -1:
                    print("Не удалось запустить: нет свободной памяти")
                else:
                    print(f"Запущен процесс с PID={pid}")
        elif command == "ps":
            processes = sys_ps(current_user)
            for p in processes:
                print(p)
        elif command == "kill":
            if not arg:
                print("Укажите PID процесса")
            else:
                try:
                    pid = int(arg)
                except ValueError:
                    print("PID должен быть числом")
                    continue
                if sys_kill(pid, current_user):
                    print(f"Процесс {pid} завершён")
                else:
                    print(f"Не удалось завершить процесс {pid}")
        elif command == "mem":
            info = kernel_instance.memory_info()
            print(f"Использовано: {info['used']} / {info['limit']} МБ")
            print(f"Свободно: {info['free']} МБ")
        elif command == "exit":
            print("Завершение работы...")
            break
        else:
            print(f"Команда не найдена: {command}")


if __name__ == "__main__":
    main()