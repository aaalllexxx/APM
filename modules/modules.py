__help__ = "Просмотреть список модулей проекта"
import os
from rich import print

def run(*args, **kwargs):
    modules = []
    if os.path.exists(".apm/installed"):
        modules = [file.replace(".py", "") for file in os.listdir(".apm/installed")]
    if modules:
        print("[blue]Установленные модули:[/blue]")
        for module in modules:
            print(f"[green] - {module}[/green]")
    else:
        print("[red][-] Нет установленных модулей[/red]")
