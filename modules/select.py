__help__ = "Выбор проекта в качестве глобального"

import os
from json_dict import JsonDict
from rich import print


def run(base_dir, gconf_path, *args, **kwargs):
    arg = kwargs["args"]
    if len(arg) == 1 or "-h" in arg:
        print("Usage: apm select")
    if os.path.isdir(".apm"):
        config = JsonDict(gconf_path)
        local_config = JsonDict(".apm/run.json")
        config.project_name = local_config.project_name
        config.main_file = local_config.main_file
        print("[green][+] Проект помечен основным[/green]")
    else:
        print("[red][-] Текущая директория не является проектом AEngine.[/red]")
        print("[red][-] Используйте 'apm init' для инициализации.[/red]")
    