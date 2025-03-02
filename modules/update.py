__help__ = "Обновить менеджер проектов apm"
import os
import zipfile
import requests
import shutil
from tqdm import tqdm
from rich import print


def run(base_dir, *args, **kwargs):
    print("[green bold][+] Начало установки исходников...[/green bold]")
    link = "https://github.com/aaalllexxx/APM/archive/refs/heads/master.zip"
    response = requests.get(link, stream=True)
    app_data = os.getenv("APPDATA")
    if not os.path.exists(app_data + os.sep +"apm" + os.sep + "sources"):
        os.mkdir(app_data + os.sep +"apm" + os.sep + "sources")

    file = open(app_data + os.sep +"apm" + os.sep + "sources" + os.sep +"master.zip", "wb")
    try:
        with tqdm.wrapattr(file, "write",
                    miniters=1, desc="Установка исходников",
                    total=int(response.headers.get('content-length', 0))) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)
    except:
        print("[red bold][-] Не удалось установить исходники [/red bold]")
        return
    file.close()
    print("[green bold][+] Исходники установлены [/green bold]")

    print("[green bold][+] Начало распаковки исходников... [/green bold]")
    os.mkdir(app_data + os.sep +"apm" + os.sep + "sources" + os.sep + "master")
    try:
        with zipfile.ZipFile(app_data + os.sep +"apm" + os.sep + "sources" + os.sep + "master.zip", 'r') as zip_ref:
            zip_ref.extractall(app_data + os.sep +"apm" + os.sep + "sources" + os.sep + "master")
    except:
        print("[red bold][-] Не удалось распаковать исходники [/red bold]")
        return

    print("[green bold][+] Исходники распакованы [/green bold]")

    print("[green bold][+] Обновление исполняемого файла... [/green bold]")
    with open(app_data + os.sep +"apm" + os.sep + "apm.exe", "wb") as file_to, open(app_data + os.sep +"apm" + os.sep + "sources" + os.sep + "master" + os.sep + "APM-master" + os.sep + "executable" + os.sep + "apm.exe", "rb") as file_from:
        file_to.write(file_from.read())
    print("[green bold][+] Исполняемый файл обновлен [/green bold]")

    print("[green bold][+] Удаление временных файлов [/green bold]")
    for file in os.listdir(app_data + os.sep +"apm" + os.sep + "sources"):
        if os.path.isfile(app_data + os.sep +"apm" + os.sep + "sources" + os.sep + file):
            os.remove(app_data + os.sep +"apm" + os.sep + "sources" + os.sep + file)
        else:
            shutil.rmtree(app_data + os.sep +"apm" + os.sep + "sources" + os.sep + file)
    os.rmdir(app_data + os.sep +"apm" + os.sep + "sources")
    print("[green bold][+] Удаление окончено [/green bold]")
    print("[green bold][+] Обновление завершено [/green bold]")
