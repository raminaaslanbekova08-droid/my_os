"""Командная оболочка StudyOS."""

from src.syscalls import (
    sys_login, sys_logout, sys_whoami,
    sys_create_file, sys_read_file, sys_delete_file, sys_list_files,
    sys_exec, sys_ps, sys_kill, sys_logs,
)
from src.kernel import kernel_instance


BANNER = """
============================================================
  StudyOS — учебная операционная система
  Введите help, чтобы увидеть список команд.
============================================================
"""

HELP = """
Доступные команды:
  help              — справка
  echo <текст>      — вывести текст
  whoami            — текущий пользователь
  login             — войти
  logout            — выйти
  create            — создать файл
  cat <путь>        — прочитать файл
  ls [путь]         — список файлов
  delete <путь>     — удалить файл
  run <имя>         — запустить процесс
  ps                — список процессов
  kill <pid>        — завершить процесс
  mem               — состояние памяти
  logs [n]          — последние n записей журнала
  exit              — выход
"""


def main():
    current_user = "guest"
    print(BANNER)
    print(f"Текущий пользователь: {current_user}")

    while True:
        try:
            raw = input(f"{current_user}@studyos:~$ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            break

        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "exit":
            print("Завершение работы оболочки.")
            break

        elif cmd == "help":
            print(HELP)

        elif cmd == "echo":
            print(arg)

        elif cmd == "whoami":
            print(sys_whoami(current_user))

        elif cmd == "login":
            login = input("Логин: ")
            password = input("Пароль: ")
            if sys_login(login, password, current_user):
                current_user = login
                print(f"Вы вошли как {login}")
            else:
                print("Ошибка входа")

        elif cmd == "logout":
            sys_logout(current_user)
            current_user = "guest"
            print("Вы вышли из системы")

        elif cmd == "create":
            path = input("Путь: ")
            content = input("Содержимое: ")
            fid = sys_create_file(path, content, current_user)
            if fid == -1:
                print("Файл с таким путём уже существует")
            else:
                print(f"Создан файл с id={fid}")

        elif cmd == "cat":
            if not arg:
                print("Укажите путь к файлу")
            else:
                content = sys_read_file(arg, current_user)
                print(content if content else "(файл пуст или не существует)")

        elif cmd == "ls":
            files = sys_list_files(arg or "/", current_user)
            if not files:
                print("(нет файлов)")
            else:
                for f in files:
                    print(f"  {f}")

        elif cmd == "delete":
            if not arg:
                print("Укажите путь к файлу")
            else:
                if sys_delete_file(arg, current_user):
                    print("Файл удалён")
                else:
                    print("Нет прав на удаление или файл не найден")

        elif cmd == "run":
            if not arg:
                print("Укажите имя программы")
            else:
                pid = sys_exec(arg, current_user)
                if pid == -1:
                    print("Не удалось запустить: нет свободной памяти")
                else:
                    print(f"Запущен процесс с PID={pid}")

        elif cmd == "ps":
            procs = sys_ps(current_user)
            if not procs:
                print("(нет процессов)")
            else:
                for p in procs:
                    print(f"  PID={p['pid']} | {p['name']} | "
                          f"state={p['state']} | owner={p['owner']} | "
                          f"mem={p['memory_used']} МБ")

        elif cmd == "kill":
            if not arg:
                print("Укажите PID")
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

        elif cmd == "mem":
            info = kernel_instance.memory_info()
            print(f"Использовано: {info['used']} / {info['limit']} МБ")
            print(f"Свободно: {info['free']} МБ")

        elif cmd == "logs":
            n = int(arg) if arg.isdigit() else 10
            rows = sys_logs(n, current_user)
            for r in rows:
                print(f"  [{r['timestamp']}] {r['syscall_name']} | "
                      f"{r['user']} | {r['status']}")

        else:
            print(f"Неизвестная команда: {cmd}. Введите help.")


if __name__ == "__main__":
    main()