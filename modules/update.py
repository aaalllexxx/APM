__help__ = "Обновить менеджер проектов apm"
import os
import shutil
import errno
import stat
from rich import print
from git import Repo  


def clear_dir(path):
    shutil.rmtree(path, ignore_errors=False, onerror=handle_remove_readonly)


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

    print("[green bold][+] Обновление исполняемого файла... [/green bold]")
    with open(app_data + os.sep +"apm" + os.sep + "apm.exe", "wb") as file_to, open(app_data + os.sep +"apm" + os.sep + "sources" + os.sep + "executable" + os.sep + "apm.exe", "rb") as file_from:
        file_to.write(file_from.read())
    print("[green bold][+] Исполняемый файл обновлен [/green bold]")

    print("[green bold][+] Удаление временных файлов [/green bold]")
    for file in os.listdir(app_data + os.sep +"apm" + os.sep + "sources"):
        try:
            if os.path.isfile(app_data + os.sep +"apm" + os.sep + "sources" + os.sep + file):
                os.remove(app_data + os.sep +"apm" + os.sep + "sources" + os.sep + file)
            else:
                clear_dir(app_data + os.sep +"apm" + os.sep + "sources" + os.sep + file)
        except Exception as e:
            print(e)
    os.rmdir(app_data + os.sep +"apm" + os.sep + "sources")
    print("[green bold][+] Удаление окончено [/green bold]")
    print("[green bold][+] Обновление завершено [/green bold]")
