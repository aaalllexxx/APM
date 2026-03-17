__help__ = "Обновление AEngineApps в текущем проекте"
__module_type__ = "ПРОЕКТЫ"

import os
import shutil
from rich import print
from git import Repo, exc
from helpers import clear_dir


def run(base_dir, *args, **kwargs):
    arg = kwargs.get("args", [])
    if "-h" in arg:
        print("Usage: apm upgrade")
        print("Скачивает последнюю версию AEngineApps из репозитория и заменяет текущую в проекте.")
        return
        
    if not os.path.exists(".apm"):
        print("[red][-] Текущая директория не является проектом AEngine ([bold].apm[/bold] не найден).[/red]")
        return
        
    print("[green][+] Подготовка к обновлению AEngineApps...[/green]")
    target_dir = os.path.join(os.getcwd(), "AEngineApps")
    
    if os.path.exists(target_dir):
        print("[yellow][*] Удаление старой версии фреймворка...[/yellow]")
        try:
            # Используем ignore_errors=True для обхода прав доступа в Windows (попытка удалить read-only файлы git)
            shutil.rmtree(target_dir, ignore_errors=True)
            if os.path.exists(target_dir):
                 print("[red][-] Не удалось удалить папку. Убедитесь, что файлы не используются в IDE или запущенном процессе.[/red]")
                 return
        except Exception as e:
            print(f"[red][-] Ошибка при удалении старой версии: {e}[/red]")
            return
            
    print("[green][*] Загрузка последней версии AEngineApps из репозитория (aaalllexxx/AEngineApps)...[/green]")
    try:
        Repo.clone_from("https://github.com/aaalllexxx/AEngineApps", target_dir)
        clear_dir(os.path.join(target_dir, ".git"))
        print("[bold green]✓ Фреймворк успешно интегрирован / обновлен на последнюю версию![/bold green]")
    except exc.GitError as e:
        print(f"[red][-] Ошибка загрузки AEngineApps: {e}[/red]")
        print("[yellow][!] Требуется Git и подключение к интернету.[/yellow]")
