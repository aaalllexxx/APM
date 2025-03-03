import os
import shutil
import errno
import stat
from rich import print

print("[green bold][+] Скрипт запущен [/green bold]")

def clear_dir(path):
    shutil.rmtree(path, ignore_errors=False, onerror=handle_remove_readonly)


def handle_remove_readonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise
app_data = os.getenv("APPDATA")
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