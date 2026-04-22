import os
import subprocess
import tempfile
    
class System:
    name = "windows" if os.name == "nt" else "linux"
    
    @classmethod
    def get_config_dir(cls):
        """Get platform-specific config directory"""
        if cls.name == "windows":
            appdata = os.getenv('APPDATA')
            if not appdata:
                # Fallback if APPDATA is not set
                appdata = os.path.expanduser('~/AppData/Roaming')
            return os.path.join(appdata, 'apm')
        else:
            return os.path.expanduser('~/.config/apm')
    
    @classmethod
    def get_temp_file(cls, filename="apm_goto.tmp"):
        """Get platform-specific temporary file path"""
        return os.path.join(tempfile.gettempdir(), filename)

    @classmethod
    def clear(cls):
        if cls.name == "windows":
            os.system("cls")
        else:
            os.system("clear")
    
    @classmethod
    def run(cls, win_command, lin_command, env=None):
        if cls.name == "windows":
            try:
                subprocess.check_call(win_command, shell=True, env=env)
            except FileNotFoundError:
                subprocess.run(win_command, shell=True, env=env)
        else:
            try:
                subprocess.check_call(lin_command, shell=True, env=env)
            except FileNotFoundError:
                subprocess.run(lin_command, shell=True, env=env)
    