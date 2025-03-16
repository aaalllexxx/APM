__help__ = "Создание файла конфигураций для проекта"

import json
from rich import print
from helpers import ConfigInput
from win2lin import System

def run(base_dir, *args, **kwargs):
    arg = kwargs["args"]
    if "-h" in arg:
        print("Usage: apm config")
        return
    try:
        config = ConfigInput.start(base_dir + "/config_template.json")
        with open("config.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(config, indent=4, ensure_ascii=False))
        System.clear()
        print("[green][+] Файл создан[/green]")
    except KeyboardInterrupt as e:
        System.clear()
        print("[red][-] Завершаю работу...[/red]")