"""APM — AEngine Package Manager."""

from argparse import ArgumentParser
import os
import sys
from importlib import import_module
from importlib.machinery import SourceFileLoader


def get_config_dir():
    """Get platform-specific config directory"""
    if os.name == 'nt':  # Windows
        return os.getenv('APPDATA') + os.sep
    else:  # Linux/macOS
        return os.path.expanduser('~/.config/')


sys.dont_write_bytecode = True
appdata = get_config_dir()
base_dir = appdata + "apm" + os.sep if os.path.exists(appdata + "apm") else os.path.dirname(os.path.abspath(__file__)) + os.sep
gconf_path = os.path.join(appdata, "apm", "global_config.json")
module_path = "modules"
install_module_path = "installed"

if not os.path.exists(os.path.join(appdata, "apm")):
    os.makedirs(os.path.join(appdata, "apm"), exist_ok=True)

if not os.path.exists(gconf_path):
    with open(gconf_path, "w") as file:
        file.write("{}")


def get_commands():
    """Загружает доступные команды и группирует их."""
    commands = {}
    for prog_name in os.listdir(os.path.join(base_dir, "modules")):
        if prog_name.startswith("__"):
            continue
        name = prog_name.split(".")[0]
        try:
            mod = import_module(f"{module_path}.{name}")
            commands[name] = getattr(mod, "__help__", "")
        except Exception:
            commands[name] = ""
    return commands


def print_help(commands):
    """Красивый вывод help с группировкой."""
    try:
        from rich.console import Console
        from rich.table import Table
        
        console = Console()
        
        console.print("\n  [bold green]AEngine Package Manager[/bold green] [dim]v2.0[/dim]\n")
        
        # Группировка команд
        project_cmds = ["create", "init", "delete", "run", "config", "select", "upgrade"]
        nav_cmds = ["goto", "list"]
        module_cmds = ["install", "remove", "modules", "develop"]
        other_cmds = ["update", "docs", "unregister"]
        
        groups = [
            ("Проект", project_cmds, "cyan"),
            ("Навигация", nav_cmds, "green"),
            ("Модули", module_cmds, "yellow"),
            ("Прочее", other_cmds, "magenta"),
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
                console.print(f"  [bold {color}]{group_name}[/bold {color}]")
                console.print(table)
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


if __name__ == "__main__":
    try:
        executable = sys.argv[1]
        args = sys.argv[1:]
        
        if executable in ("-h", "--help", "help"):
            print_help(get_commands())
        else:
            try:
                import_module(f"{module_path}.{executable}").run(base_dir, gconf_path, args=args)
            except ModuleNotFoundError as e:
                try:
                    module = SourceFileLoader(
                        f"{install_module_path}.{executable}.{args[1]}",
                        os.getcwd() + os.sep + ".apm" + os.sep + "installed" + os.sep + executable + os.sep + args[1] + ".py"
                    ).load_module()
                    module.run(base_dir)
                except Exception:
                    try:
                        import_module(f"{install_module_path}.{executable}.{args[1]}").run(base_dir, gconf_path, args=args)
                    except (ModuleNotFoundError, IndexError):
                        print(f"Команда {executable} не опознана.")
                    except AttributeError:
                        import_module(f"{install_module_path}.{executable}").run(base_dir)

            except AttributeError:
                print(f"Команда {executable} пока не реализована.") 
                
    except IndexError:
        print_help(get_commands())
