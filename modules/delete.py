__help__ = "Удаление проекта"
import os
import shutil
from helpers import input
from rich import print
from helpers import clear_dir

def run(*args, **kwargs):
    arg = kwargs["args"]
    if len(arg) == 1 or "-h" in arg:
        print("Usage: apm delete")
    if os.path.isdir(".apm"):
        dir_name = os.getcwd()
        os.chdir(os.path.dirname(dir_name))
        try:
            clear_dir(dir_name)
        except PermissionError:
            print("[red][-] Не получилось удалить все файлы.\nВозможно что-то придется удалить вручную.[/red]")
    else:
        print("[red][-] Текущая директория не является проектом AEngine.[/red]")
        print("[red][-] Используйте 'apm init' для инициализации.[/red]")