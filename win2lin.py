import os
import subprocess
from typing import Self
    
class System:
    name = "windows" if os.name == "nt" else "linux"
    
    @classmethod
    def clear(cls):
        if cls.name == "windows":
            os.system("cls")
        else:
            os.system("clear")
    
    @classmethod
    def run(cls, win_command, lin_command):
        if cls.name == "windows":
            try:
                subprocess.check_call(win_command)
            except FileNotFoundError:
                subprocess.run(win_command)
        else:
            try:
                subprocess.check_call(lin_command)
            except FileNotFoundError:
                subprocess.run(lin_command)
    