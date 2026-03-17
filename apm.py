"""APM — AEngine Package Manager."""

from argparse import ArgumentParser
import os
import sys
import importlib
import importlib.util

def get_config_dir():
    """Get platform-specific config directory"""
    return os.path.dirname(os.path.abspath(__file__)) + os.sep

sys.dont_write_bytecode = True
base_dir = get_config_dir()
gconf_path = os.path.join(base_dir, "global_config.json")
module_path = "modules"
install_module_path = "installed"

if not os.path.exists(gconf_path):
    with open(gconf_path, "w") as file:
        file.write("{}")

def get_commands():
    """Загружает доступные команды и группирует их."""
    commands = {}
    modules_dir = os.path.join(base_dir, "modules")
    if not os.path.isdir(modules_dir):
        return commands
    for prog_name in os.listdir(modules_dir):
        if prog_name.startswith("__"):
            continue
        name = prog_name.split(".")[0]
        try:
            mod = importlib.import_module(f"{module_path}.{name}")
            commands[name] = getattr(mod, "__help__", "")
        except Exception as e:
            # Показываем имя модуля, но не падаем — чтобы help работал даже при сломанных модулях
            commands[name] = f"[ошибка загрузки: {e}]"
    return commands


def print_help(commands):
    """Красивый вывод help с группировкой."""
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        
        console = Console()
        
        console.print("\n  [bold green]AEngine Package Manager[/bold green] [dim]v2.0[/dim]\n")
        
        # Группировка команд
        project_cmds = ["create", "init", "delete", "run", "config", "select", "upgrade"]
        nav_cmds = ["goto", "list"]
        module_cmds = ["install", "remove", "modules", "develop"]
        other_cmds = ["update", "docs", "unregister"]
        
        groups = [
            ("ПРОЕКТЫ", project_cmds, "cyan"),
            ("НАВИГАЦИЯ", nav_cmds, "green"),
            ("МОДУЛИ", module_cmds, "yellow"),
            ("ПРОЧЕЕ", other_cmds, "magenta"),
        ]
        
        for group_name, cmd_list, color in groups:
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column(style=f"bold {color}", width=14)
            table.add_column(style="white")
            
            has_items = False
            for cmd in cmd_list:
                if cmd in commands:
                    has_items = True
                    table.add_row(cmd, commands[cmd])
            
            if has_items:
                # Рисуем красивую панель с заголовком
                console.print(Panel(table, title=f"[bold {color}]{group_name}[/bold {color}]", title_align="left", expand=False))
                console.print()
        
        # Показать незнакомые команды
        known = set()
        for _, cmd_list, _ in groups:
            known.update(cmd_list)
        unknown = {k: v for k, v in commands.items() if k not in known}
        if unknown:
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column(style="bold white", width=14)
            table.add_column(style="white")
            for cmd, desc in unknown.items():
                table.add_row(cmd, desc)
            console.print(f"  [bold white]Другое[/bold white]")
            console.print(table)
            console.print()
            
    except ImportError:
        # Fallback без rich
        print("\nИспользование: apm <опции> <флаги>\n")
        print("Доступные опции:")
        for name, desc in commands.items():
            print(f"    {name} - {desc}")


def _load_module_from_file(name, filepath):
    """Загружает Python-модуль из файла через importlib (без deprecated load_module)."""
    spec = importlib.util.spec_from_file_location(name, filepath)
    if spec is None or spec.loader is None:
        raise ImportError(f"Не удалось загрузить спецификацию модуля: {filepath}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    try:
        executable = sys.argv[1]
        args = sys.argv[1:]
        
        if executable in ("-h", "--help", "help"):
            print_help(get_commands())
        else:
            try:
                importlib.import_module(f"{module_path}.{executable}").run(base_dir, gconf_path, args=args)
            except ModuleNotFoundError as e:
                # Ключевая проверка: если e.name совпадает с запрашиваемым модулем —
                # значит сам модуль не найден. Если e.name другое — ошибка внутри модуля
                # (не хватает зависимости).
                expected_module = f"{module_path}.{executable}"
                if e.name == expected_module or e.name == executable:
                    # Модуль APM не найден — пробуем загрузить как локальный (.apm/installed/)
                    try:
                        local_module_dir = os.path.join(os.getcwd(), ".apm", "installed", executable)
                        
                        if not os.path.exists(local_module_dir):
                            print(f"Команда '{executable}' не найдена.")
                            print(f"  Используйте 'apm --help' для списка доступных команд.")
                            sys.exit(1)

                        if len(args) < 2:
                            module_file = os.path.join(local_module_dir, "init.py")
                            if not os.path.exists(module_file):
                                module_file = os.path.join(local_module_dir, "__init__.py")
                        else:
                            module_file = os.path.join(local_module_dir, args[1] + ".py")
                        
                        if os.path.exists(module_file):
                            if local_module_dir not in sys.path:
                                sys.path.insert(0, local_module_dir)
                                
                            module = _load_module_from_file(f"{executable}.subcommand", module_file)
                            
                            if hasattr(module, "run"):
                                module.run(base_dir, gconf_path=gconf_path, args=args[2:] if len(args) > 1 else [])
                            else:
                                print(f"[!] В модуле {module_file} не найдена функция run()")
                        else:
                            print(f"Команда '{executable}' не найдена.")
                            print(f"  Используйте 'apm --help' для списка доступных команд.")
                    
                    except ModuleNotFoundError as inner_e:
                        import traceback
                        print(f"[!] Ошибка зависимости при загрузке '{executable}': отсутствует модуль '{inner_e.name}'")
                        traceback.print_exc()
                    except Exception:
                        import traceback
                        print(f"[!] Ошибка при выполнении команды '{executable}':")
                        traceback.print_exc()
                else:
                    # Модуль APM найден, но внутри него ошибка импорта — показываем реальную ошибку
                    import traceback
                    print(f"[!] Ошибка при выполнении '{executable}': отсутствует модуль '{e.name}'")
                    print(f"    Установите его: pip install {e.name}")
                    traceback.print_exc()

            except AttributeError:
                print(f"Команда '{executable}' пока не реализована.") 
            except Exception:
                import traceback
                print(f"[!] Ошибка при выполнении команды '{executable}':")
                traceback.print_exc()
                
    except IndexError:
        print_help(get_commands())
