__help__ = "Установка программных модулей"
from git import Repo
from helpers import clear_dir
import os

def run(base_dir, *args, **kwargs):
    arg:list = kwargs["args"]
    url = arg[arg.index("-u") + 1] if "-u" in arg else  arg[arg.index("--url") + 1] if "--url" in args else arg[1]
    name = url.split("/")[-1].replace(".git", "")
    if not os.path.exists("installed"):
        os.mkdir("installed")
    Repo.clone_from(url, f"installed/{name}")
    clear_dir(f"installed/{name}/.git")
    