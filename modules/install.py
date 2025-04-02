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
    url = arg[arg.index("--url") + 1] if "--url" in args else arg[-1] if "github.com" in arg[-1] else ""
    if not url:
        url = f"https://github.com/{arg[-2]}/{arg[-1]}"
    name = url.split("/")[-1].replace(".git", "")
    path = ".apm/installed"
    if "-g" in arg:
        arg.remove("-g")
        path = base_dir + "installed"
    elif not os.path.exists(".apm"):
        print("[red][-] Директория не является проектом AEngine[/red]")
        return
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        if update and os.path.exists(f"{path}/{name}"):
            clear_dir(f"{path}/{name}")
        Repo.clone_from(url, f"{path}/{name}")
    except exc.GitError:
        print(f"[red][-] {url} не является репозиторием git[/red]")
        return
    clear_dir(f"{path}/{name}/.git")
    print("[green][+] Модуль установлен[/green]")
    