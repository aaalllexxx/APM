import os
import time
import cursor
from keyboard import add_hotkey, block_key, is_pressed, unblock_key
from rich import print
from json_dict import JsonDict
from win2lin import System

standard_input = input

def input(msg):
    print(f"[green bold]{msg}\n-> [/green bold]", end="")
    return standard_input()

def block_controls():
    block_key("return")
    block_key("up")
    block_key("down")

def unblock_controls():
    unblock_key("return")
    unblock_key("up")
    unblock_key("down")

class FileInput:
    index = 0
    content = [".."] + os.listdir()
    changed = True
    
    @classmethod
    def set_defaults(cls):
        cls.index = 0
        cls.content = [".."] + os.listdir()
        cls.changed = True

    @classmethod
    def change_index(cls, size):
        System.clear()
        cls.index -= size
        if cls.index > len(cls.content) -1:
            cls.index = 0
        cls.changed = True
    
    @classmethod 
    def select_file(cls):
        current = cls.content[cls.index]
        try:
            block_key("enter")
            System.clear()
            selected = None
            path = ""
            add_hotkey("down", cls.change_index, args=[-1], suppress=True) 
            add_hotkey("up", cls.change_index, args=[1], suppress=True)
            cursor.hide()
            waits_return = True
            while not selected:
                if is_pressed("return") and waits_return:
                    if current == "..":
                        cls.index = 0
                        path = "/".join(path.strip("/").split("/")[:-1])
                        cls.content = [".."] + os.listdir(path if path else None)
                        cls.changed = True
                        waits_return = False
                    elif os.path.isfile(path + current):
                        selected = path + current
                        unblock_key("enter")
                        cls.set_defaults()
                        return selected
                    else:
                        path += current + "/"
                        cls.content = [".."] + os.listdir(path)
                        cls.index = 0
                        cls.changed = True
                        waits_return = False
                    System.clear()
                elif not is_pressed("return"):
                    waits_return = True
                if cls.changed:
                    print("Выберите файл:\n")
                    current = cls.content[cls.index]
                    for file in cls.content:
                        if file == current:
                            print(f"[green]> {file}[/green]")
                        else:
                            print(f"[lightgray]{file}[/lightgray]")
                    print(f"\n[bold red]{path + current}[/bold red]")
                    cls.changed = False
        except KeyboardInterrupt:
            unblock_key("enter")
            cursor.show()
        except Exception as e:
            unblock_key("enter")
            print(cls.content, cls.index, current)
            print(e)
        cls.set_defaults()

class ConfigInput:
    config = {}

    @classmethod
    def __input_options(cls, variants):
        selected = False
        index = 0
        pressed = False
        changed = True
        block_controls()
        while not selected: 
            if changed and not pressed:
                System.clear()
                print("[green bold]Выберите опцию:[/green bold]\n")
                for i, v in enumerate(variants):
                    if i == index:
                        print(f"{i+ 1}) [white]> {v}[/white]")
                    else:
                        print(f"{i+1}) [red]{v}[/red]")
                changed = False
            if is_pressed("down"):
                if not pressed:
                    index += 1
                if index >= len(variants):
                    index = 0
                changed = True
                pressed = True
            elif is_pressed("up"):
                if not pressed:
                    index -= 1
                if index < 0:
                    index = len(variants) - 1
                changed = True
                pressed = True
            elif is_pressed("enter"):
                changed = False
                unblock_controls()
                return variants[index]
            else:
                pressed = False
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
        if data["type"] == "int":
            cls.config[key] = int(input("Введите целое число:")) or data["default"]
        elif data["type"] == "str":
            cls.config[key] = input("Введите строку:") or data["default"]
        elif data["type"] == "bool":
            cls.config[key] = cls.__input_options([True, False]) or data["default"]
        elif data["type"] == "select":
            cls.config[key] = cls.__input_options(data["options"]) or data["default"]
        elif data["type"] == "dict":
            cls.config[key] = cls.__input_dict() or data["default"]

    @classmethod
    def start(cls, template):
        block_controls()
        template = JsonDict(template)
        index = 0
        configured = False
        pressed = True
        changed = True
        while not configured:
            if changed and not pressed:
                System.clear()
                print("[green bold]Выберите настройку [blue bold](esc, чтобы закончить)[/blue bold]:[/green bold]\n")
                for k, v in template.dictionary.items():
                    if k == template.keys()[index]:
                        conf = cls.config.get(k)
                        print(f"{index + 1}) [white]> {k}: [blue]{conf if conf is not None else v['default']}[/blue] -> {v.get('help') or 'Неизвестно'}[/white]")
                    else:
                        conf = cls.config.get(k)
                        print(f"{template.keys().index(k) + 1}) [red]{k}: {conf if conf is not None else v['default']}[/red]")
                print()
                changed = False
            if is_pressed("up"):
                if not pressed:
                    index -= 1
                if index < 0:
                    index = len(template.keys()) -1
                pressed = True
                changed = True
            elif is_pressed("down"):
                if not pressed:
                    index += 1
                if index >= len(template.keys()):
                    index = 0
                pressed = True
                changed = True
            elif is_pressed("enter"):
                i = template.keys()[index]
                time.sleep(0.2)
                unblock_controls()
                cls.input(i, template[i])
                block_controls()
                time.sleep(0.2)
                pressed = True
                changed = True
            elif is_pressed("esc"):
                unblock_controls()
                return cls.config

            else:
                pressed = False
        unblock_controls()