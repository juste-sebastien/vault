from cgitb import text
import main

from vault.account import Account
from vault.vault import Vault
import vault.zip as arch

import functionalities.delete as func_del
import functionalities.generate as func_gen

from kivy.core.window import Window

from kivy.metrics import dp, sp

from kivy.properties import StringProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, NoTransition

from kivymd.app import MDApp

from kivymd.uix.button import MDIconButton, MDRectangleFlatButton
from kivymd.uix.screen import MDScreen


VAULT = Vault("try", "try")

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


class ConsultScreen(MDScreen):
    def __init__(self, **kwargs):
        self.account_list =  {}
        self.test_list = ["test.csv", "test2.csv", "test3.csv"]
        super(ConsultScreen, self).__init__(**kwargs)

    def get_list_account(self):
        main_grid = self.ids.consult_grid
        main_grid.clear_widgets()
        for file in self.test_list:
            text_button = file.strip(".csv")
            account = Account("text_button", "test", "test", "test.com")
            account_button = MDRectangleFlatButton(id=text_button,text=text_button, font_size=sp(12), padding=(0, 0, dp(5),0), size_hint=(0.8, 0.8), pos_hint={"center_x": 0, "center_y": 0.5})
            trash_id = text_button + "_trash"
            trash_icon = MDIconButton(id=trash_id, icon="delete-outline", padding=(0, 0, dp(5),0), size_hint=(0.10, 0.8), pos_hint={"center_x": 0.5, "center_y": 0.5})
            trash_icon.bind(on_press=self.remove)
            refresh_id = text_button + "_refresh"
            refresh_icon = MDIconButton(id=refresh_id, icon="refresh", padding=(0, 0, dp(5),0), size_hint=(0.10, 0.8), pos_hint={"center_x": 0.5, "center_y": 0.5})
            refresh_icon.bind(on_press=self.refresh)
            main_grid.add_widget(trash_icon)
            main_grid.add_widget(refresh_icon)
            main_grid.add_widget(account_button)
            account.widgets["trash"] = trash_icon
            account.widgets["refresh"] = refresh_icon
            account.widgets["button"] = account_button
            self.account_list[text_button] = account
            print(self.account_list)


    def remove(self, instance):
        account_name, icon = str(instance.id).split("_")
        if account_name in self.account_list.keys():
            current_account = self.account_list[account_name]
            trash = current_account.widgets.get("trash")
            self.ids.consult_grid.remove_widget(trash)
            refresh = current_account.widgets.get("refresh")
            self.ids.consult_grid.remove_widget(refresh)
            acnt_button = current_account.widgets.get("button")
            self.ids.consult_grid.remove_widget(acnt_button)
            filename = account_name + ".csv"
            #func_del.remove_file(file=filename, vault=VAULT)
            self.account_list.pop(account_name)
            #VAULT.content.pop(filename)
            self.test_list.pop(self.test_list.index(filename))

    def refresh(self, instance):
        pass


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
        sm.add_widget(ConsultScreen(name="consult"))
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