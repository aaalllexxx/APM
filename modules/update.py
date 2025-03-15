__help__ = "Обновить менеджер проектов apm"
import os
import subprocess
from rich import print
from git import Repo 
import shutil
import errno
import stat


def clear_dir(path):
    shutil.rmtree(path, ignore_errors=False, onexc=handle_remove_readonly)


def handle_remove_readonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

def run(base_dir, *args, **kwargs):
    print("[green bold][+] Начало установки исходников...[/green bold]")
    link = "https://github.com/aaalllexxx/APM/"
    app_data = os.getenv("APPDATA")
    try:
        if os.path.exists(app_data + os.sep +"apm" + os.sep + "sources"):
            clear_dir(app_data + os.sep +"apm" + os.sep + "sources")
        os.mkdir(app_data + os.sep +"apm" + os.sep + "sources")
    except Exception as e:
        input(e)
    Repo.clone_from(link, app_data + os.sep +"apm" + os.sep + "sources")
    
    print("[green bold][+] Исходники установлены [/green bold]")
    print("[green bold][+] Запуск скрипта обновления [/green bold]")
    subprocess.run(["cmd.exe", "/c", "start", app_data + os.sep + "apm/sources/executable/update.exe"])
