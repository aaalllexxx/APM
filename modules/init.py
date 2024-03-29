__help__ = "Регистрация проекта в качестве проекта AEngine"

import json
import os
import cursor
from win2lin import System
from helpers import input, FileInput
from rich import print


def run(*args, **kwargs):
    project_name = input("Введите название проекта:")
    
    print()
    
    answer = input("Сменить главный файл проекта с main.py? [д/н]")
    
    if "д" in answer or "y" in answer:
        launch_file = FileInput.select_file()
        
    else:
        launch_file = "main.py"
        
    if launch_file:
        data = {
            "project_name": project_name,
            "main_file": os.path.abspath(launch_file)
        }
        if not os.path.exists(".apm"):
            os.mkdir(".apm")
            
        if not os.path.exists(".apm/installed"):
            os.mkdir(".apm/installed")
            
        with open(".apm/run.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
    System.clear()
    print("[green bold]Проект инициализирован.[/green bold]")
    
    
cursor.show()