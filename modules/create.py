__help__ = "Создание нового проекта"

import json
import os
import shutil
from rich import print
from win2lin import System
from helpers import input, clear_dir, register_project
from git import Repo, exc


def run(base_dir, *args, **kwargs):
    arg = kwargs["args"]
    if "-h" in arg:
        print("Usage: apm create")
        return
    path = input("Введите название проекта:")
    if not path or not path.strip():
        print("[red][-] Название проекта не может быть пустым.[/red]")
        return
    
    print("[green][+] Создание проекта...[/green]")
    directory = os.path.join(os.getcwd(), path.replace(" ", "_"))
    
    if os.path.exists(directory):
        print(f"[red][-] Директория '{directory}' уже существует.[/red]")
        return
    
    template_dir = os.path.join(base_dir, "examples", "default_project")
    if not os.path.exists(template_dir):
        print(f"[red][-] Шаблон проекта не найден: {template_dir}[/red]")
        return
    
    try:
        shutil.copytree(template_dir, directory)
    except OSError as e:
        print(f"[red][-] Ошибка при копировании шаблона: {e}[/red]")
        return
    
    os.chdir(directory)
    data = {
            "project_name": path,
            "main_file": os.path.abspath("main.py")
        }
    if not os.path.exists(".apm"):
        os.mkdir(".apm")
        
    if not os.path.exists(".apm/installed"):
        os.mkdir(".apm/installed")
    
    try:
        Repo.clone_from("https://github.com/aaalllexxx/AEngineApps", os.path.join(directory, "AEngineApps"))
        clear_dir("AEngineApps/.git")
    except exc.GitError as e:
        print(f"[yellow][!] Не удалось загрузить AEngineApps: {e}[/yellow]")
        print("[yellow][!] Установите вручную: apm install https://github.com/aaalllexxx/AEngineApps[/yellow]")
        
    try:
        with open(".apm/run.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
    except OSError as e:
        print(f"[red][-] Ошибка при сохранении конфигурации: {e}[/red]")
        return
    
    # Регистрация проекта в глобальном конфиге
    gconf_path = args[0] if args else os.path.join(base_dir, "global_config.json")
    register_project(gconf_path, path, directory)
    
    print("[green bold]Проект создан.[/green bold]")