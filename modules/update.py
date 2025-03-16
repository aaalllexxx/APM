__help__ = "Обновить менеджер проектов apm"
import os
import subprocess
from rich import print
from git import Repo
from helpers import clear_dir

def run(base_dir, *args, **kwargs):
    arg = kwargs["args"]
    if "-h" in arg:
        print("Usage: apm update")
        return
    print("[green bold][+] Начало установки исходников...[/green bold]")
    link = "https://github.com/aaalllexxx/APM/"
    app_data = os.getenv("APPDATA")
    try:
        if os.path.exists(app_data + os.sep +"apm" + os.sep + "sources"):
            clear_dir(app_data + os.sep +"apm" + os.sep + "sources")
        os.mkdir(app_data + os.sep +"apm" + os.sep + "sources")
    except Exception as e:
        input(e)
    for file in os.listdir(app_data + os.sep + "apm"):
        file = app_data + os.sep + "apm" + os.sep + file
        try:
            if os.path.isfile(file):
                os.remove(file)
            else:
                clear_dir(file)
        except:
            pass
    Repo.clone_from(link, app_data + os.sep +"apm" + os.sep + "sources")
    
    print("[green bold][+] Исходники установлены [/green bold]")
    print("[green bold][+] Запуск скрипта обновления [/green bold]")
    subprocess.run(["cmd.exe", "/c", "start", app_data + os.sep + "apm/sources/scripts/setup.bat", "2>", "NULL"])
    print("[green bold][+] Готово. Дождитесь выполнения скрипта. [/green bold]")

