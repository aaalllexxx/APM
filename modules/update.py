"""Модуль обновления APM из репозитория."""

__help__ = "Обновить менеджер проектов apm"
__module_type__ = "ПРОЧЕЕ"

import os
from rich import print
from git import Repo, exc
from helpers import clear_dir
from win2lin import System

# Файлы и директории, которые НЕ должны удаляться при обновлении
_PROTECTED_NAMES = frozenset({
    "installed",
    "global_config.json",
    "config.json",
})

# Только эти расширения файлов могут быть удалены
_ALLOWED_EXTENSIONS = frozenset({
    ".py", ".bat", ".sh", ".ps1", ".md", ".txt", ".json",
})


def _is_safe_to_delete(filepath, apm_dir):
    """Проверяет безопасность удаления файла/директории.

    Args:
        filepath: Абсолютный путь к файлу/директории.
        apm_dir: Базовая директория APM.

    Returns:
        True если файл можно безопасно удалить.
    """
    real_filepath = os.path.realpath(filepath)
    real_apm_dir = os.path.realpath(apm_dir)

    # Проверяем что путь находится внутри директории APM
    if not real_filepath.startswith(real_apm_dir + os.sep):
        return False

    basename = os.path.basename(filepath)

    # Защита важных файлов/директорий
    if basename in _PROTECTED_NAMES:
        return False

    # Для файлов проверяем расширение
    if os.path.isfile(filepath):
        _, ext = os.path.splitext(basename)
        if ext.lower() not in _ALLOWED_EXTENSIONS:
            return False

    return True


def run(base_dir, gconf_path, *args, **kwargs):
    """Обновляет APM из GitHub-репозитория.

    Args:
        base_dir: Базовая директория APM.
        gconf_path: Путь к глобальному конфигу APM.
    """
    arg = kwargs["args"]
    if "-h" in arg:
        print("Usage: apm update")
        return
    print("[green bold][+] Начало установки исходников...[/green bold]")
    link = "https://github.com/aaalllexxx/APM/"
    config_dir = System.get_config_dir()
    apm_dir = config_dir

    if not os.path.exists(apm_dir):
        print(f"[red][-] Директория APM не найдена: {apm_dir}[/red]")
        return

    # Безопасная очистка старых файлов
    for file in os.listdir(apm_dir):
        fl = os.path.join(apm_dir, file)
        if not _is_safe_to_delete(fl, apm_dir):
            continue
        try:
            if os.path.isfile(fl):
                os.remove(fl)
            elif os.path.isdir(fl):
                clear_dir(fl)
        except Exception as e:
            print(f"[yellow][!] Не удалось удалить {fl}: {e}[/yellow]")

    sources_dir = os.path.join(apm_dir, "sources")
    if os.path.exists(sources_dir):
        try:
            clear_dir(sources_dir)
        except Exception:
            pass

    try:
        Repo.clone_from(link, sources_dir)
    except exc.GitError as e:
        print(f"[red][-] Ошибка загрузки исходников: {e}[/red]")
        print("[red]    Проверьте подключение к интернету.[/red]")
        return
    
    print("[green bold][+] Исходники установлены [/green bold]")
    print("[green bold][+] Запуск скрипта обновления [/green bold]")
    
    setup_bat = os.path.join(apm_dir, "sources", "scripts", "setup.bat")
    setup_sh = os.path.join(apm_dir, "sources", "scripts", "setup.sh")
    
    try:
        System.run(
            f'cmd.exe /c start "" "{setup_bat}"',
            f'bash "{setup_sh}"'
        )
    except Exception as e:
        print(f"[red][-] Ошибка запуска скрипта обновления: {e}[/red]")
        return
    
    print("[green bold][+] Готово. Дождитесь выполнения скрипта. [/green bold]")
