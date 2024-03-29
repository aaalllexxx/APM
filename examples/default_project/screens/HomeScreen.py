from AEngineApps.screen import Screen
from flask import render_template

class HomeScreen(Screen):
    def run(self):
        return render_template("index.html")