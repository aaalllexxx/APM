__help__ = "Создание нового проекта"

import json
import os
import shutil
from rich import print
from win2lin import System
from helpers import input, clear_dir
from git import Repo


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
    
    os.chdir(path)
    Repo.clone_from("https://github.com/aaalllexxx/AEngineApps", "AEngineApps")
    clear_dir("AEngineApps/.git")
        
    with open(".apm/run.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))
    print("[green bold]Проект создан.[/green bold]")