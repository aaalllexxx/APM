import os
import time
import cursor
from rich import print
from json_dict import JsonDict
from win2lin import System
import shutil
import errno
import stat

# Cross-platform keyboard handling
# keyboard library requires root on Linux, so we use fallback
if os.name == 'nt':
    try:
        from keyboard import add_hotkey, block_key, is_pressed, unblock_key
        KEYBOARD_AVAILABLE = True
    except ImportError:
        KEYBOARD_AVAILABLE = False
else:
    KEYBOARD_AVAILABLE = False

# Fallback functions when keyboard is not available
def _dummy_add_hotkey(*args, **kwargs): pass
def _dummy_block_key(*args, **kwargs): pass
def _dummy_is_pressed(*args, **kwargs): return False
def _dummy_unblock_key(*args, **kwargs): pass

if not KEYBOARD_AVAILABLE:
    add_hotkey = _dummy_add_hotkey
    block_key = _dummy_block_key
    is_pressed = _dummy_is_pressed
    unblock_key = _dummy_unblock_key


def clear_dir(path):
    shutil.rmtree(path, ignore_errors=False, onexc=handle_remove_readonly)


def handle_remove_readonly(func, path, exc):
  excvalue = exc
  if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise


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
    def _select_file_text_mode(cls):
        """Text-based file selection for Linux/when keyboard is unavailable"""
        path = ""
        while True:
            System.clear()
            content = [".."] + os.listdir(path if path else None)
            print("[green bold]Выберите файл (введите номер или 'q' для выхода):[/green bold]\n")
            for i, file in enumerate(content):
                prefix = "[DIR]" if os.path.isdir(os.path.join(path, file) if file != ".." else "..") else "[FILE]"
                if file == "..":
                    prefix = "[UP]"
                print(f"  {i}) {prefix} {file}")
            
            choice = standard_input("\n-> ")
            if choice.lower() == 'q':
                return None
            try:
                idx = int(choice)
                if 0 <= idx < len(content):
                    selected = content[idx]
                    if selected == "..":
                        path = "/".join(path.strip("/").split("/")[:-1])
                    elif os.path.isfile(os.path.join(path, selected)):
                        return os.path.join(path, selected) if path else selected
                    else:
                        path = os.path.join(path, selected) if path else selected
            except ValueError:
                pass
    
    @classmethod 
    def select_file(cls):
        # Use text mode on Linux (no keyboard library)
        if not KEYBOARD_AVAILABLE:
            return cls._select_file_text_mode()
        
        # Original Windows implementation with keyboard hotkeys
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
    def __input_options_text_mode(cls, variants):
        """Text-based option selection for Linux/when keyboard is unavailable"""
        System.clear()
        print("[green bold]Выберите опцию:[/green bold]\n")
        for i, v in enumerate(variants):
            print(f"  {i + 1}) {v}")
        while True:
            try:
                choice = int(standard_input("\n-> ")) - 1
                if 0 <= choice < len(variants):
                    return variants[choice]
            except ValueError:
                pass
            print("[red]Неверный выбор, попробуйте снова[/red]")

    @classmethod
    def __input_options(cls, variants):
        # Use text mode on Linux (no keyboard library)
        if not KEYBOARD_AVAILABLE:
            return cls.__input_options_text_mode(variants)
        
        # Original Windows implementation
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
    def _start_text_mode(cls, template):
        """Text-based config editor for Linux/when keyboard unavailable"""
        template = JsonDict(template)
        for tmpl in template.keys():
            if template[tmpl].get("required"):
                cls.config[tmpl] = template[tmpl]["default"]
        
        while True:
            System.clear()
            print("[green bold]Выберите настройку (введите номер или 'q' для завершения):[/green bold]\n")
            keys = template.keys()
            for i, k in enumerate(keys):
                v = template[k]
                conf = cls.config.get(k)
                print(f"  {i + 1}) {k}: [blue]{conf if conf is not None else v['default']}[/blue] -> {v.get('help') or 'Неизвестно'}")
            
            choice = standard_input("\n-> ")
            if choice.lower() == 'q':
                return cls.config
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(keys):
                    key = keys[idx]
                    cls.input(key, template[key])
            except ValueError:
                pass

    @classmethod
    def start(cls, template):
        # Use text mode on Linux (no keyboard library)
        if not KEYBOARD_AVAILABLE:
            return cls._start_text_mode(template)
        
        # Original Windows implementation
        block_controls()
        template = JsonDict(template)
        for tmpl in template.keys():
            if template[tmpl].get("required"):
                cls.config[tmpl] = template[tmpl]["default"]
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