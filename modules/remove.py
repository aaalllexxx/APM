__help__ = "удаляет загруженный модуль"
import os
from helpers import clear_dir
from rich import print

def run(base_dir, *args, **kwargs):
    arg:list = kwargs["args"]
    module = arg[-1]
    path = ".apm/installed"
    if "-g" in arg:
        arg.pop(arg.index("-g"))
        path = base_dir + "installed"

    if not os.path.exists(".apm"):
        print("[red][-] Директория не является проектом apm[/red]")
        return
    if not os.path.exists(f".apm/installed/{module}"):
        print("[red][-] Модуль не найден[/red]")
        return
    
    clear_dir(f"{path}/{module}")
    print("[green][+] Модуль удален[/green]")