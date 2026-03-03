__help__ = "Запуск проекта AEngine"


import json
import os

from rich import print
from helpers import System, input, FileInput


def run(base_dir, gconf_path, *args, **kwargs):
    arg = kwargs["args"]
    if "-h" in arg:
        print("Usage: apm run")
        return
    
    try:
        with open(gconf_path, encoding="utf-8") as file_config:
            g_config = json.loads(file_config.read() or "{}")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[red][-] Ошибка чтения глобальной конфигурации: {e}[/red]")
        g_config = {}
                
    if os.path.exists(".apm/run.json"):
        try:
            with open(".apm/run.json", encoding="utf-8") as file:
                data = json.loads(file.read())
        except json.JSONDecodeError as e:
            print(f"[red][-] Ошибка чтения .apm/run.json: {e}[/red]")
            return
    
    elif g_config.get("project_name"):
        data = g_config
    
    else:
        print("[red][-] Текущая директория не является проектом AEngine.[/red]")
        print("[red][-] Используйте 'apm init' или 'apm select' в проекте.[/red]")
        return
    
    if "project_name" not in data:
        print("[red][-] В конфигурации не указано имя проекта (project_name).[/red]")
        return
    
    if "main_file" not in data:
        print("[red][-] В конфигурации не указан главный файл (main_file).[/red]")
        return

    print(f"[green][+] Запуск проекта '{data['project_name']}'...[/green]")
    try:
        interpreter = g_config.get("interpreter")
        file = data["main_file"].replace(" ", '" "')
        System.run(f'{interpreter or "python"} {file}', 
                    f'{interpreter or "python3"} {file}')
        print(f"[green][+] Проект '{data['project_name']}' отработал успешно.[/green]")

    except FileNotFoundError:
        print("[red][-] Интерпретатор Python не найден.[/red]")
        ans = input("Выбрать другой интерпретатор? [д/н]")
        if "y" in ans or "д" in ans:
            selected = FileInput.select_file()
            if selected:
                interp = os.path.abspath(selected)
                g_config["interpreter"] = interp
                try:
                    with open(os.path.join(base_dir, "global_config.json"), "w", encoding="utf-8") as file_config:
                        file_config.write(json.dumps(g_config, indent=4, ensure_ascii=False))
                    print(f"[green][+] Интерпретатор сохранён: {interp}[/green]")
                except OSError as e:
                    print(f"[red][-] Не удалось сохранить конфигурацию: {e}[/red]")
            else:
                print("[yellow][!] Файл не выбран.[/yellow]")
    except Exception as e:
        print(f"[red][-] Ошибка при запуске проекта: {e}[/red]")
        ans = input("Выбрать другой интерпретатор? [д/н]")
        if "y" in ans or "д" in ans:
            selected = FileInput.select_file()
            if selected:
                interp = os.path.abspath(selected)
                g_config["interpreter"] = interp
                try:
                    with open(os.path.join(base_dir, "global_config.json"), "w", encoding="utf-8") as file_config:
                        file_config.write(json.dumps(g_config, indent=4, ensure_ascii=False))
                    print(f"[green][+] Интерпретатор сохранён: {interp}[/green]")
                except OSError as e:
                    print(f"[red][-] Не удалось сохранить конфигурацию: {e}[/red]")
            else:
                print("[yellow][!] Файл не выбран.[/yellow]")