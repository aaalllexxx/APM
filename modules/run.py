__help__ = "Запуск проекта AEngine"


import json
import os

from rich import print
from helpers import System, input, FileInput


def run(base_dir, gconf_path, *args, **kwargs):
    arg = kwargs["args"]
    if len(arg) == 1 or "-h" in arg:
        print("Usage: apm run")
    with open(gconf_path, encoding="utf-8") as file_config:
                g_config = json.loads(file_config.read() or "{}")
                
    if os.path.exists(".apm/run.json"):
        with open(".apm/run.json", encoding="utf-8") as file:
            data = json.loads(file.read())
    
    elif os.path.exists(gconf_path):
        with open(gconf_path, encoding="utf-8") as file:
            data = json.loads(file.read())
    
    else:
        print("[red][-] Файл конфигурации не найден.[/red]")
        return
            
    print(f"[green][+] Запуск проекта '{data['project_name']}'...[/green]")
    try:
        interpreter = g_config.get("interpreter")
        file = data["main_file"].replace(" ", '" "')
        System.run(f'{interpreter or "python"} {file}', 
                    f'{interpreter or "python3"} {file}')
        print(f"[green][+] Проект '{data['project_name']}' отработал успешно.[/green]")

        
        
    except Exception as e:
        ans = input("[red][-] Случилась ошибка. Выбрать другой интерпретатор?[/red]")
        if "y" in ans or "д" in ans:
            interp = os.path.abspath(FileInput.select_file())
        
            g_config["interpreter"] = interp
            with open(base_dir + "global_config.json", "w", encoding="utf-8") as file_config:
                file_config.write(json.dumps(g_config, indent=4, ensure_ascii=False))
        