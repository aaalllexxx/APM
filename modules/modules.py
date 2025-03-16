__help__ = "Просмотреть список модулей проекта"
import os
from rich import print

def run(base_dir, *args, **kwargs):
    arg = kwargs["args"]
    if "-h" in arg:
        print("Usage: apm modules")
        return
    modules = []
    if os.path.exists(".apm/installed"):
        modules = [file.replace(".py", "") for file in os.listdir(".apm/installed")]
    if os.path.exists(base_dir + "installed"):
        gmodules = [file.replace(".py", "") for file in os.listdir(base_dir + "installed")]
    
    print("[blue]Модули проекта:[/blue]")
    if modules:
        for module in modules:
            print(f"[green] - {module}[/green]")
    else:
        print("[red][-] Нет установленных модулей[/red]\n")
    print("[blue]Глобальные модули:[/blue]")
    if gmodules:
        for module in gmodules:
            print(f"[green] - {module}[/green]")
    else:
        print("[red][-] Нет установленных модулей[/red]\n")
