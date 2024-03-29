import os
import cursor
from keyboard import add_hotkey, block_key, is_pressed, unblock_key
from rich import print

from win2lin import System

standard_input = input

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

def input(msg):
    print(f"[green bold]{msg}\n-> [/green bold]", end="")
    return standard_input()