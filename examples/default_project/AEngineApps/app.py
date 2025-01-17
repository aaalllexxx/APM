import os
from flask import Flask
from AEngineApps.json_dict import JsonDict
from importlib import import_module
import webview

class App:
    def __init__(self, app_name=__name__, debug=False):
        self.app_name = app_name
        self.project_root = os.path.dirname(os.path.dirname(__file__)) + os.sep
        self.flask = Flask(self.app_name)
        self.flask.debug = debug
        self.flask.root_path = self.project_root
        self.__config = {}
        self.window = None
    
    def add_router(self, path: str, view_func: callable, **options):
        self.flask.add_url_rule(path, view_func=view_func, **options)
        
    def add_routers(self, rules: dict[str, callable]):
        for route, func in rules.items():
            self.add_router(route, func)
            
    def load_config(self, path, encoding="utf-8"):
        self.config = JsonDict(path, encoding)
    
    def run(self):
        self.window = webview.create_window(self.app_name, self.flask)
        webview.start(debug=self.config.get("debug") or False)
                
    def close(self):
        if self.window:
            self.window.destroy()
          
    @property
    def config(self) -> dict:
        return self.__config
    
    @config.setter
    def config(self, value):
        if isinstance(value, dict):
            if value.get("routes"):
                for route, func in value["routes"].items():
                    if value.get("screen_path"):
                        prefix = value["screen_path"].replace("/", ".") + "."
                    cls = getattr(import_module(prefix + func), func)
                    options = {}
                    if hasattr(cls, "__options__"):
                        options = cls.__options__
                    call = cls()
                    self.add_router(route, call, **options)
            
            if value.get("root_path"):
                self.flask.root_path = value["root_path"]
            for prop, value in value.items():       
                self.__config[prop] = value
        
        elif isinstance(value, JsonDict):
            self.config = value.dictionary