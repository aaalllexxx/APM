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
    
    # 1. Загрузка встроенных модулей (APM/modules/)
    modules_dir = os.path.join(base_dir, "modules")
    if os.path.isdir(modules_dir):
        for prog_name in os.listdir(modules_dir):
            if prog_name.startswith("__") or not prog_name.endswith(".py"):
                continue
            name = prog_name.split(".")[0]
            try:
                mod = importlib.import_module(f"{module_path}.{name}")
                desc = getattr(mod, "__help__", "")
                mod_type = getattr(mod, "__module_type__", "ПРОЧЕЕ")
                commands[name] = {"help": desc, "type": mod_type}
            except Exception as e:
                commands[name] = {"help": f"[ошибка загрузки: {e}]", "type": "ОШИБКИ"}

    # 2. Загрузка локальных пользовательских модулей (.apm/installed/)
    local_installed_dir = os.path.join(os.getcwd(), ".apm", "installed")
    if os.path.isdir(local_installed_dir):
        for name in os.listdir(local_installed_dir):
            mod_dir = os.path.join(local_installed_dir, name)
            if not os.path.isdir(mod_dir):
                continue
            
            # Пропускаем, если такой модуль уже есть (встроенный имеет приоритет)
            if name in commands:
                continue
                
            # Ищем точку входа (init.py или __init__.py)
            entry_file = os.path.join(mod_dir, "init.py")
            if not os.path.exists(entry_file):
                entry_file = os.path.join(mod_dir, "__init__.py")
                
            if os.path.exists(entry_file):
                try:
                    mod = _load_module_from_file(f"local_{name}", entry_file)
                    desc = getattr(mod, "__help__", f"Локальный модуль {name}")
                    mod_type = getattr(mod, "__module_type__", "ЛОКАЛЬНЫЕ ПЛАГИНЫ")
                    commands[name] = {"help": desc, "type": mod_type}
                except Exception as e:
                    commands[name] = {"help": f"[ошибка локального модуля: {e}]", "type": "ОШИБКИ"}

    return commands


def print_help(commands):
    """Красивый вывод help с группировкой."""
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        
        console = Console()
        
        console.print("\n  [bold green]AEngine Package Manager[/bold green] [dim]v2.0[/dim]\n")
        
        # Динамическая группировка команд
        groups_data = {}
        for cmd, data in commands.items():
            mod_type = data["type"].upper()
            if mod_type not in groups_data:
                groups_data[mod_type] = []
            groups_data[mod_type].append((cmd, data["help"]))
            
        # Цвета для популярных групп, остальные случайные из палитры
        color_map = {
            "ПРОЕКТЫ": "cyan",
            "НАВИГАЦИЯ": "green",
            "МОДУЛИ": "yellow",
            "ПРОЧЕЕ": "magenta",
            "ОШИБКИ": "red"
        }
        fallback_colors = ["blue", "dark_orange", "purple", "dark_sea_green", "steel_blue"]
        
        # Сортировка групп: Проекты, Навигация, Модули... Ошибки в конце
        order_priority = {"ПРОЕКТЫ": 0, "НАВИГАЦИЯ": 1, "МОДУЛИ": 2, "ПРОЧЕЕ": 98, "ОШИБКИ": 99}
        sorted_groups = sorted(groups_data.keys(), key=lambda k: order_priority.get(k, 50))
        
        color_idx = 0
        for group_name in sorted_groups:
            cmd_list = groups_data[group_name]
            
            color = color_map.get(group_name)
            if not color:
                color = fallback_colors[color_idx % len(fallback_colors)]
                color_idx += 1
                
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column(style=f"bold {color}", width=14)
            table.add_column(style="white")
            
            for cmd, desc in sorted(cmd_list):
                table.add_row(cmd, desc)
                
            console.print(Panel(table, title=f"[bold {color}]{group_name}[/bold {color}]", title_align="left", expand=False))
            console.print()
            
    except ImportError:
        # Fallback без rich
        print("\nИспользование: apm <опции> <флаги>\n")
        print("Доступные опции:")
        for name, data in commands.items():
            print(f"    {name} - {data['help']} ({data['type']})")


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
