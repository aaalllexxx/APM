__help__ = "Установка программных модулей"
from git import Repo, exc
from helpers import clear_dir
import os
from rich import print

def run(base_dir, *args, **kwargs):
    arg:list = kwargs["args"]
    if "-h" in arg:
        print("Usage: apm install <flags> <url>\n    -u - Обновить указанный модуль\n    --url - Указать репозиторий\n    -g - Установить модуль глобально")
        return
    update = "-u" in arg
    if update:
        arg.remove("-u")
    
    try:
        url = arg[arg.index("--url") + 1] if "--url" in arg else arg[-1] if "github.com" in arg[-1] else ""
        if not url:
            if len(arg) >= 3:
                url = f"https://github.com/{arg[-2]}/{arg[-1]}"
            else:
                print("[red][-] Не указан URL репозитория.[/red]")
                print("[yellow]Использование: apm install <url> или apm install <owner> <repo>[/yellow]")
                return
    except (IndexError, ValueError):
        print("[red][-] Неверный формат команды.[/red]")
        print("[yellow]Использование: apm install <url> или apm install --url <url>[/yellow]")
        return
    
    name = url.split("/")[-1].replace(".git", "")
    if not name:
        print("[red][-] Не удалось определить имя модуля из URL.[/red]")
        return
    
    path = ".apm/installed"
    if "-g" in arg:
        arg.remove("-g")
        path = base_dir + "installed"
    elif not os.path.exists(".apm"):
        print("[red][-] Директория не является проектом AEngine[/red]")
        return
    
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            print(f"[red][-] Не удалось создать директорию: {e}[/red]")
            return
    
    try:
        if update and os.path.exists(f"{path}/{name}"):
            clear_dir(f"{path}/{name}")
        print(f"[green][+] Загрузка модуля '{name}'...[/green]")
        Repo.clone_from(url, f"{path}/{name}")
    except exc.GitError as e:
        print(f"[red][-] Ошибка загрузки: {url}[/red]")
        print(f"[red]    Убедитесь, что URL верный и есть доступ к сети.[/red]")
        return
    
    try:
        git_dir = f"{path}/{name}/.git"
        if os.path.exists(git_dir):
            clear_dir(git_dir)
    except Exception as e:
        print(f"[yellow][!] Не удалось удалить .git: {e}[/yellow]")
    
    print("[green][+] Модуль установлен[/green]")