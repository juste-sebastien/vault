import main

from vault.vault import Vault
import vault.zip as arch

import functionalities.generate as func_gen

from kivy.core.window import Window

from kivy.metrics import dp

from kivy.properties import StringProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, NoTransition

from kivymd.app import MDApp

from kivymd.uix.screen import MDScreen


VAULT = ""

class LoginScreen(MDScreen):
    def on_click(self, login, pwd):
        VAULT = Vault(login, pwd)
        #arch.undo_zip(vault)
        self.manager.transition.direction = "left"
        self.manager.current = "welcome"

    def clear(self):
        self.ids.login.text = ""
        self.ids.pwd.text = ""


class WelcomeScreen(MDScreen):
    def print_usages_warns(self):
        return f"{main.WARNS}\n{main.USAGE}"


class GenerateScreen(MDScreen):
    pwd = StringProperty("")
    def __init__(self, **kwargs):
        self.custom_list = func_gen.ALPHABET
        super(GenerateScreen, self).__init__(**kwargs)

    def add_digits_to_list(self, widget):
        if widget.active and widget.name == "digits":
            self.custom_list += func_gen.DIGIT
        else:
            self.custom_list = [x for x in self.custom_list if x not in func_gen.DIGIT]

    def add_spec_to_list(self, widget):
        if widget.active and widget.name == "spec_char":
            self.custom_list += func_gen.SPEC_CHARS
        else:
            self.custom_list = [x for x in self.custom_list if x not in func_gen.SPEC_CHARS]

    
    def do_generate(self, widget):
        self.pwd = func_gen.generate(widget.value, self.custom_list)
        return self.pwd


class ModifyScreen(MDScreen):
    pass

class LogoutScreen(MDScreen):
    pass
    

class AddScreen(MDScreen):
    pass


class DelScreen(MDScreen):
    pass


class UpdateScreen(MDScreen):
    pass


class VaultApp(MDApp):
    Window.size = (400, 700)
    def build(self):
        self.title = "[Vault App] by Cabron"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(GenerateScreen(name="generate"))
        sm.add_widget(ModifyScreen(name="modify"))
        sm.add_widget(LogoutScreen(name="logout"))
        sm.add_widget(AddScreen(name="add"))
        sm.add_widget(DelScreen(name="delete"))
        sm.add_widget(UpdateScreen(name="update"))
        return sm

    def change_screen(self, **kwargs):
        print(kwargs["screen"].name)
        if "Logout" in kwargs["widget"].text:
            #arch.save(VAULT)
            kwargs["screen"].manager.transition.direction = "left"
            kwargs["screen"].manager.current = "login"
        elif kwargs["widget"].text in ["Add", "Delete", "Update"]:
            kwargs["screen"].manager.transition = NoTransition()
            kwargs["screen"].manager.current = str(kwargs["widget"].text).lower()
        else:
            kwargs["screen"].manager.transition.direction = "left"
            kwargs["screen"].manager.current = str(kwargs["widget"].text).lower()

        

def run():
    VaultApp().run()