import os
import sys
import json
import cursor
from rich import print
from json_dict import JsonDict
from win2lin import System
import shutil
import errno
import stat
import readchar


def register_project(gconf_path, name, path):
    """Регистрирует проект в глобальном конфиге APM (без дубликатов)."""
    try:
        with open(gconf_path, encoding="utf-8") as f:
            g_config = json.loads(f.read() or "{}")
    except (FileNotFoundError, json.JSONDecodeError):
        g_config = {}
    
    projects = g_config.get("projects", [])
    if not any(p.get("path") == path for p in projects):
        projects.append({"name": name, "path": path})
        g_config["projects"] = projects
        try:
            with open(gconf_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(g_config, indent=4, ensure_ascii=False))
        except OSError as e:
            print(f"[yellow][!] Не удалось зарегистрировать проект: {e}[/yellow]")


def clear_dir(path):
    if not os.path.exists(path):
        return
    try:
        if sys.version_info >= (3, 12):
            shutil.rmtree(path, ignore_errors=False, onexc=handle_remove_readonly)
        else:
            shutil.rmtree(path, ignore_errors=False, onerror=handle_remove_readonly_legacy)
    except Exception as e:
        print(f"[red][-] Ошибка при удалении '{path}': {e}[/red]")
        raise


def handle_remove_readonly(func, path, exc):
  excvalue = exc
  if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise


def handle_remove_readonly_legacy(func, path, exc_info):
  excvalue = exc_info[1]
  if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise excvalue


standard_input = input

def input(msg):
    print(f"[green bold]{msg}\n-> [/green bold]", end="")
    return standard_input()


def _render_list(items, index, title=None):
    """Отрисовка списка с выделенным элементом"""
    System.clear()
    if title:
        print(title)
    for i, item in enumerate(items):
        if i == index:
            print(f"[green]> {item}[/green]")
        else:
            print(f"  [white]{item}[/white]")


class FileInput:
    @classmethod
    def select_file(cls):
        path = ""
        index = 0
        try:
            cursor.hide()
            while True:
                content = [".."] + os.listdir(path if path else None)
                if index >= len(content):
                    index = 0
                
                System.clear()
                print(f"Выберите файл [green bold](esc - отмена)[/green bold]:\n")
                for i, file in enumerate(content):
                    if i == index:
                        print(f"[green]> {file}[/green]")
                    else:
                        print(f"  [white]{file}[/white]")
                print(f"\n[bold red]{os.path.join(path, content[index]) if path else content[index]}[/bold red]")

                key = readchar.readkey()
                
                if key == readchar.key.UP:
                    index = (index - 1) % len(content)
                elif key == readchar.key.DOWN:
                    index = (index + 1) % len(content)
                elif key == readchar.key.ENTER or key == readchar.key.CR:
                    current = content[index]
                    if current == "..":
                        index = 0
                        path = os.path.dirname(path.rstrip("/\\"))
                    elif os.path.isfile(os.path.join(path, current) if path else current):
                        cursor.show()
                        return os.path.join(path, current) if path else current
                    else:
                        path = os.path.join(path, current) if path else current
                        index = 0
                elif key == readchar.key.ESC:
                    cursor.show()
                    return None
        except KeyboardInterrupt:
            cursor.show()
            return None


class ConfigInput:
    config = {}

    @classmethod
    def __input_options(cls, variants):
        index = 0
        while True:
            _render_list(
                [str(v) for v in variants], 
                index,
                "[green bold]Выберите опцию:[/green bold]\n"
            )
            
            key = readchar.readkey()
            
            if key == readchar.key.UP:
                index = (index - 1) % len(variants)
            elif key == readchar.key.DOWN:
                index = (index + 1) % len(variants)
            elif key == readchar.key.ENTER or key == readchar.key.CR:
                return variants[index]
            elif key == readchar.key.ESC:
                return None

    @classmethod
    def __input_dict(cls):
        System.clear()
        d = {}
        route = input("Введите ключ (s для сохранения, e для выхода):")
        while not route:
            route = input("Необходим ключ (s для сохранения, e для выхода):")
        
        if route == "e":
            return None
        
        if route == "s":
            return d
        
        screen = input("Введите значение (e для выхода):")
        while not screen:
            screen = input("Необходимо значение (e для выхода):")

        while route not in ["s", "e"] and screen not in ["s", "e"]:
            System.clear()
            d[route] = screen
            for k, v in d.items():
                print(f"[green]{k}[/green]: [blue]{v}[/blue]")
            
            route = input("Введите ключ (s для сохранения, e для выхода):")
            while not route:
                route = input("Необходим ключ (s для сохранения, e для выхода):")

            if route == "e":
                return None
            
            if route == "s":
                return d
            
            screen = input("Введите значение (e для выхода):")
            while not screen:
                screen = input("Необходимо значение (e для выхода):")
        return None



    @classmethod
    def input(cls, key, data):
        try:
            if data["type"] == "int":
                raw = input("Введите целое число:")
                try:
                    cls.config[key] = int(raw) if raw else data["default"]
                except ValueError:
                    print(f"[red][-] '{raw}' не является числом, используется значение по умолчанию.[/red]")
                    cls.config[key] = data["default"]
            elif data["type"] == "str":
                cls.config[key] = input("Введите строку:") or data["default"]
            elif data["type"] == "bool":
                cls.config[key] = cls.__input_options([True, False]) or data["default"]
            elif data["type"] == "select":
                cls.config[key] = cls.__input_options(data["options"]) or data["default"]
            elif data["type"] == "dict":
                if data.get("default") == "auto":
                    mode = cls.__input_options(["Автоматическая", "Ручная"])
                    if mode == "Автоматическая":
                        cls.config[key] = "auto"
                    elif mode == "Ручная":
                        result = cls.__input_dict()
                        cls.config[key] = result if result else data["default"]
                    else:
                        pass
                else:
                    cls.config[key] = cls.__input_dict() or data["default"]
            else:
                print(f"[yellow][!] Неизвестный тип '{data['type']}' для '{key}', пропускаю.[/yellow]")
        except KeyboardInterrupt:
            print("\n[yellow][!] Ввод отменён.[/yellow]")

    @classmethod
    def start(cls, template, existing=None):
        template = JsonDict(template)
        cls.config = dict(existing) if existing else {}
        for tmpl in template.keys():
            if template[tmpl].get("required") and tmpl not in cls.config:
                cls.config[tmpl] = template[tmpl]["default"]
        index = 0
        
        while True:
            System.clear()
            print("[green bold]Выберите настройку [blue bold](Ctrl+S - сохранить, esc - выйти)[/blue bold]:[/green bold]\n")
            for k, v in template.dictionary.items():
                ki = template.keys().index(k)
                conf = cls.config.get(k)
                if ki == index:
                    print(f"{ki + 1}) [white]> {k}: [blue]{conf if conf is not None else v['default']}[/blue] -> {v.get('help') or 'Неизвестно'}[/white]")
                else:
                    print(f"{ki + 1}) [red]{k}: {conf if conf is not None else v['default']}[/red]")
            print()

            key = readchar.readkey()
            
            if key == readchar.key.UP:
                index = (index - 1) % len(template.keys())
            elif key == readchar.key.DOWN:
                index = (index + 1) % len(template.keys())
            elif key == readchar.key.ENTER or key == readchar.key.CR:
                i = template.keys()[index]
                cursor.show()
                cls.input(i, template[i])
            elif key == readchar.key.CTRL_S:
                return cls.config
            elif key == readchar.key.ESC:
                print("[yellow][!] Выход без сохранения.[/yellow]")
                return None