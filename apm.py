from argparse import ArgumentParser
import os
import sys
from importlib import import_module
import sys

sys.dont_write_bytecode = True
base_dir = os.sep.join(__file__.split(os.sep)[:-1]) + os.sep
appdata = os.getenv('APPDATA') + os.sep
gconf_path = appdata + "apm" + os.sep + "global_config.json"
module_path = "modules"
install_module_path = "installed"
available_commands = []
helps = []

if not os.path.exists(appdata + "apm"):
    os.mkdir(appdata + "apm")

if not os.path.exists(gconf_path):
    with open(gconf_path, "w") as file:
        file.write("{}")
for prog_name in os.listdir(os.path.join(appdata + "apm", "modules")):
    if prog_name.startswith("__"):
        continue
    name = prog_name.split(".")[0]
    try:
        available_commands.append(name + " - " + import_module(f"{module_path}.{name}").__help__.lower())
    except AttributeError:
        available_commands.append(name)        

if "apm" in " ".join(sys.argv):
    try:
        executable = sys.argv[1]
        try:
            module = import_module(f"{module_path}.{executable}").run(appdata + "apm", gconf_path)
        except ModuleNotFoundError as e:
            print(e)
            try:
                module = import_module(f"{install_module_path}.{executable}").run(appdata + "apm")
            except (AttributeError, ModuleNotFoundError) as e:
                print(f"Команда {executable} не опознана.")
        except AttributeError:
            print(f"Команда {executable} пока не реализована.") 
                
    except IndexError:
        print("\nИспользование: apm <опции> <флаги>\n")
        print("Доступные опции:\n    " + "\n    ".join(available_commands))
