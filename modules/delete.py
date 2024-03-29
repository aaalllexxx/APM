__help__ = "Удаление проекта"
import os
import shutil
from helpers import input
from rich import print

def rm(path):
    path = os.path.abspath(path)
    data = os.listdir(path)
    if not data:
        for d in data:
            if os.path.isdir(d):
                rm(d)
            else:
                os.remove(d)
    else:
        os.chdir(os.path.dirname(path))
        shutil.rmtree(path)

def run(*args, **kwargs):
    if os.path.isdir(".apm"):
        dir_name = os.getcwd()
        os.chdir(os.path.dirname(dir_name))
        try:
            rm(dir_name)
        except PermissionError:
            print("[red][-] Не получилось удалить все файлы.\nВозможно что-то придется удалить вручную.[/red]")
    else:
        print("[red][-] Текущая директория не является проектом AEngine.[/red]")
        print("[red][-] Используйте 'apm init' для инициализации.[/red]")