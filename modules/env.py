__help__ = "Выполнить команду внутри окружения APM"
__module_type__ = "ПРОЧЕЕ"

import os
import subprocess
import sys

from rich import print


def _build_apm_env():
    env = os.environ.copy()

    python_executable = sys.executable
    venv_dir = os.path.dirname(os.path.dirname(python_executable))
    scripts_dir = os.path.dirname(python_executable)

    env["VIRTUAL_ENV"] = venv_dir
    env["PATH"] = scripts_dir + os.pathsep + env.get("PATH", "")

    return env, python_executable


def run(base_dir, *args, **kwargs):
    arg = kwargs["args"]
    command_args = arg[1:] if arg and arg[0] == "env" else arg

    if not command_args or "-h" in command_args or "--help" in command_args:
        print(
            "Usage: apm env <command> [args...]\n"
            "Examples:\n"
            "  apm env pip install requests\n"
            "  apm env python -V\n"
            "  apm env where python"
        )
        return

    env, python_executable = _build_apm_env()

    if command_args[0] == "pip":
        command = [python_executable, "-m", "pip", *command_args[1:]]
    elif command_args[0] == "python":
        command = [python_executable, *command_args[1:]]
    else:
        command = command_args

    print(f"[cyan][*] APM env python: {python_executable}[/cyan]")

    try:
        completed = subprocess.run(command, env=env)
    except FileNotFoundError:
        print(f"[red][-] Команда не найдена: {command[0]}[/red]")
        return
    except Exception as e:
        print(f"[red][-] Ошибка выполнения команды: {e}[/red]")
        return

    if completed.returncode == 0:
        print("[green][+] Команда завершилась успешно.[/green]")
    else:
        print(f"[red][-] Команда завершилась с ошибкой (exit code {completed.returncode}).[/red]")
