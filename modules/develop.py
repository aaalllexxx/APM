__help__ = "help string"
from rich import print
from helpers import input

def run(*args, **kwargs):
    arg = kwargs["args"]
    if "-h" in arg:
        print("Usage: apm develop <template>\n    module - создать модуль")
        return
    if "module" in arg:
        base = '__help__ = "help string"\nfrom rich import print\n\ndef run(*args, **kwargs):\n\tprint(args, kwargs)'
        name = input("Введите название модуля")
        with open(f"{name}.py", "w", encoding="utf-8") as file:
            file.write(base)
        print("[green][+] Модуль создан[/green]")
        
