import main

from vault.vault import Vault
import vault.zip as arch

import functionalities.generate as func_gen

from kivy.app import App

from kivy.config import Config

from kivy.properties import StringProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginScreen(Screen):
    def on_click(self, login, pwd):
        vault = Vault(login, pwd)
        #arch.undo_zip(vault)
        self.manager.transition.direction = "left"
        self.manager.current = "welcome"


class WelcomeScreen(Screen):
    def print_usages_warns(self):
        return f"{main.WARNS}\n{main.USAGE}"

    def get_screen(self, id):
        match id:
            case "Generate":
                self.manager.transition.direction = "left"
                self.manager.current = "generate"
            case "Add":
                print("add")
                pass
            case "Modify":
                print("modify")
                pass
            case "Delete":
                print("delete")
                pass
            case "Logout":
                print("logout")
            case "Consult":
                print("consult")



class GenerateScreen(Screen):
    pwd = StringProperty("")
    def __init__(self, **kwargs):
        self.custom_list = func_gen.ALPHABET + func_gen.DIGIT + func_gen.SPEC_CHARS
        super(GenerateScreen, self).__init__(**kwargs)

    def add_to_list(self, widget, status):
        if not status and widget.name == "digits":
            self.custom_list -= func_gen.DIGIT
        if not status and widget.name == "spec_char":
            self.custom_list -= func_gen.SPEC_CHARS
    
    def do_generate(self, widget):
        self.pwd = func_gen.generate(widget.value, self.custom_list)
        return self.pwd

    def get_screen(self, screen_name):
        if "Generate" in screen_name:
            self.manager.transition.direction = "left"
            self.manager.current = "generate"



class VaultApp(App):
    Config.set("graphics", "width", "400")
    Config.set("graphics", "height", "700")
    def build(self):
        self.title = "[Vault App] by Cabron"
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(GenerateScreen(name="generate"))
        return sm


def run():
    VaultApp().run()