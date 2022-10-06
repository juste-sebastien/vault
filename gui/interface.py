import main

from vault.vault import Vault
import vault.zip as arch

import functionalities.generate as func_gen

from kivy.app import App

from kivy.config import Config

from kivy.metrics import dp

from kivy.properties import StringProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen


VAULT = ""

class LoginScreen(Screen):
    def on_click(self, login, pwd):
        VAULT = Vault(login, pwd)
        #arch.undo_zip(vault)
        self.manager.transition.direction = "left"
        self.manager.current = "welcome"


class WelcomeScreen(Screen):
    def print_usages_warns(self):
        return f"{main.WARNS}\n{main.USAGE}"

    def get_screen(self, screen_name):
        self.manager.transition.direction = "left"
        if "Logout" in screen_name:
            #arch.save(VAULT)
            self.manager.current = "login"
        else:
            self.manager.current = str(screen_name).lower()


class GenerateScreen(Screen):
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

    def get_screen(self, screen_name):
        self.manager.transition.direction = "left"
        if "Logout" in screen_name:
            #arch.save(VAULT)
            self.manager.current = "login"
        else:
            self.manager.current = str(screen_name).lower()


class ModifyScreen(Screen):
    """
    def __init__(self, **kwargs):
        self.init_layout()
        super(ModifyScreen, self).__init__(**kwargs)
        

    def init_layout(self):
        print("ok pour init layout")
        layout = GridLayout(cols=1, rows= 4, padding=dp(20))
        layout.add_widget(self.add_top_bar())

    def add_top_bar(self):
        print("ok pour top bar")
        top_boxlayout = BoxLayout(spacing=dp(20), size_hint=(0.5, None), height=dp(60), pos_hint={"center_x": 0.5})
        a_button = Button(text="Add")
        top_boxlayout.add_widget(a_button)
        d_button = Button(text="Del")
        top_boxlayout.add_widget(d_button)
        m_button = Button(text="Modif")
        top_boxlayout.add_widget(m_button)
        return top_boxlayout
    """


    def do_canvas(self, widget):
        if "Add" in widget.text:
            self.do_add_canvas()
        if "Del" in widget.text:
            self.do_del_canvas()
        if "Modif" in widget.text:
            self.do_change_canvas()

    def get_screen(self, screen_name):
        self.manager.transition.direction = "left"
        self.manager.current = str(screen_name).lower()

    def do_add_canvas(self):
        print("add_canvas")
        pass

    def do_del_canvas(self):
        print("del_canvas")
        pass

    def do_change_canvas(self):
        print("change_canvas")
        pass


class LogoutScreen(Screen):
    def get_screen(self, screen_name):
        self.manager.transition.direction = "left"
        if "Logout" in screen_name:
            #arch.save(VAULT)
            self.manager.current = "login"
        else:
            self.manager.current = str(screen_name).lower()
    

class VaultApp(App):
    Config.set("graphics", "width", "400")
    Config.set("graphics", "height", "700")
    def build(self):
        self.title = "[Vault App] by Cabron"
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(GenerateScreen(name="generate"))
        sm.add_widget(ModifyScreen(name="modify"))
        sm.add_widget(LogoutScreen(name="logout"))
        return sm


def run():
    VaultApp().run()