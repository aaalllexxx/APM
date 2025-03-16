from argparse import ArgumentParser
import os
import sys
from importlib import import_module
import sys
from importlib.machinery import SourceFileLoader


sys.dont_write_bytecode = True
appdata = os.getenv('APPDATA') + os.sep
base_dir = appdata + "apm/" if os.path.exists(appdata + "/apm") else os.sep.join(__file__.split(os.sep)[:-1]) + os.sep
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
for prog_name in os.listdir(os.path.join(base_dir, "modules")):
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
        args = sys.argv[1:]
        try:
            module = import_module(f"{module_path}.{executable}").run(base_dir, gconf_path, args=args)
        except ModuleNotFoundError as e:
            try:
                module = SourceFileLoader(f"{install_module_path}.{executable}.{args[1]}", os.getcwd() + os.sep + "installed" + os.sep + executable + os.sep + args[1] +".py").load_module()
                module = module.run(base_dir)
            except (AttributeError, ModuleNotFoundError) as e:
                print(e)
                print(f"Команда {executable} не опознана.")
        except AttributeError:
            print(f"Команда {executable} пока не реализована.") 
                
    except IndexError as e:
        print("\nИспользование: apm <опции> <флаги>\n")
        print("Доступные опции:\n    " + "\n    ".join(available_commands))
