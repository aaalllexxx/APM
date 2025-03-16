__help__ = "удаляет загруженный модуль"
import os
from helpers import clear_dir
from rich import print

def run(*args, **kwargs):
    arg = kwargs["args"]
    module = arg[1]
    if not os.path.exists(".apm"):
        print("[red][-] Директория не является проектом apm[/red]")
        return
    if not os.path.exists(f".apm/installed/{module}"):
        print("[red][-] Модуль не найден[/red]")
        return
    
    clear_dir(f".apm/installed/{module}")
    print("[green][+] Модуль удален[/green]")