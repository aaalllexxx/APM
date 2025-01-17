__help__ = "Создание нового проекта"

import json
import os
import shutil
from rich import print
from win2lin import System
from helpers import input


def run(base_dir, *args, **kwargs):
    path = input("Введите название проекта:")
    print("[green][+] Создание проекта...[/green]")
    directory = os.path.join(os.getcwd(), path.replace(" ", "_"))
    shutil.copytree(base_dir + os.sep.join(["examples", "default_project"]), directory)
    os.chdir(directory)
    data = {
            "project_name": path,
            "main_file": os.path.abspath("main.py")
        }
    if not os.path.exists(".apm"):
        os.mkdir(".apm")
        
    if not os.path.exists(".apm/installed"):
        os.mkdir(".apm/installed")
        
    with open(".apm/run.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))
    print("[green bold]Проект создан.[/green bold]")