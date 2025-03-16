__help__ = "удаляет загруженный модуль"
import os
from helpers import clear_dir
from rich import print

def run(base_dir, *args, **kwargs):
    arg: list = kwargs["args"]
    if len(arg) == 1 or "-h" in arg:
        print("Usage: apm remove <flags> <name>\n    -g - Удаление глобального модуля")
        return
    module = arg[-1]
    path = ".apm/installed"
    if "-g" in arg:
        arg.pop(arg.index("-g"))
        path = base_dir + "installed"

    elif not os.path.exists(".apm"):
        print("[red][-] Директория не является проектом apm[/red]")
        return
    
    if not os.path.exists(path):
        print("[red][-] Модуль не найден[/red]")
        return
    
    clear_dir(f"{path}/{module}")
    print("[green][+] Модуль удален[/green]")