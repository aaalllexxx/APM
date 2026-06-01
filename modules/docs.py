"""Модуль открытия документации AEngineApps."""

__help__ = "Открыть документацию AEngineApps"
__module_type__ = "ПРОЧЕЕ"

import webbrowser
from rich import print


def run(base_dir, gconf_path, *args, **kwargs):
    """Открывает документацию AEngineApps в браузере.

    Args:
        base_dir: Базовая директория APM.
        gconf_path: Путь к глобальному конфигу APM.
    """
    arg = kwargs["args"]
    if "-h" in arg:
        print("Usage: apm docs")
        return
    webbrowser.open("https://github.com/aaalllexxx/AEngineApps")