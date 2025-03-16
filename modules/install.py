__help__ = "Установка программных модулей"
from git import Repo, exc
from helpers import clear_dir
import os
from rich import print

def run(base_dir, *args, **kwargs):
    arg:list = kwargs["args"]
    url = arg[arg.index("-u") + 1] if "-u" in arg else  arg[arg.index("--url") + 1] if "--url" in args else arg[-1]
    name = url.split("/")[-1].replace(".git", "")
    path = ".apm/installed"
    if "-g" in arg:
        arg.pop(arg.index("-g"))
        if not os.path.exists(base_dir + "installed"):
            path = base_dir + "installed"
    elif not os.path.exists(".apm"):
        print("[red][-] Директория не является проектом AEngine[/red]")
        return
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        Repo.clone_from(url, f"{path}/{name}")
    except exc.GitError:
        print(f"[red][-] {url} не является репозиторием git[/red]")
        return
    clear_dir(f"{path}/{name}/.git")
    print("[green][+] Модуль установлен[/green]")
    