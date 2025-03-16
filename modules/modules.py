__help__ = "Просмотреть список модулей проекта"
import os

def run(*args, **kwargs):
    modules = []
    if os.path.exists(".apm/installed"):
        modules = [file.replace(".py", "") for file in os.listdir(".apm/installed")]
    if modules:
        print("Установленные модули:")
        for module in modules:
            print(f" - {module}")
    else:
        print("Нет установленных модулей")
