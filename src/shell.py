"""Командная оболочка StudyOS."""
import sys
from src.syscalls import sys_echo, sys_get_users

BANNER = """
========================================
  StudyOS v0.1 - учебная ОС
========================================
Введите 'help' для списка команд.
"""


def print_help():
    """Выводит справку."""
    print("""
Доступные команды:
  help   - справка
  echo   - вывести сообщение
  users  - список пользователей
  exit   - выход
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
        elif command == "echo":
            print(sys_echo(arg, current_user))
        elif command == "users":
            users = sys_get_users(current_user)
            for u in users:
                print(f"  {u[0]}: {u[1]} ({u[2]})")
        elif command == "exit":
            print("Завершение работы...")
            break
        else:
            print(f"Команда не найдена: {command}")


if __name__ == "__main__":
    main()