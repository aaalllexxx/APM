__help__ = "Просмотреть список модулей проекта"
import os
from rich import print

def run(base_dir, *args, **kwargs):
    arg = kwargs["args"]
    module = None
    if "-h" in arg:
        print("Usage: apm modules <module_name: (optional)>")
        return
    if len(arg) >= 2:
        module = arg[-1]

    modules = []
    gmodules = []
    if os.path.exists(".apm/installed"):
        if module is None:
            modules = [file.replace(".py", "") for file in os.listdir(".apm/installed") if "__" not in file and ("py" in file or os.path.isdir(f".apm/installed/{file}"))]
        elif os.path.exists(f".apm/installed/{module}"):
            modules = [file.replace(".py", "") for file in os.listdir(f".apm/installed/{module}") if "__" not in file and ("py" in file or os.path.isdir(f".apm/installed/{module}/{file}"))]

        
    if os.path.exists(base_dir + "installed"):
        if module is None:
            gmodules = [file.replace(".py", "") for file in os.listdir(base_dir + "installed") if "__" not in file and ("py" in file or os.path.isdir(f"{base_dir}installed/{file}"))]
        elif os.path.exists(f"{base_dir}installed/{module}"):
            gmodules = [file.replace(".py", "") for file in os.listdir(f"{base_dir}installed/{module}") if "__" not in file and ("py" in file or os.path.isdir(f"{base_dir}installed/{module}/{file}"))]
    
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
