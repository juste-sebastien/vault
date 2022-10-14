from turtle import onclick
from vault.account import Account
from vault.vault import Vault
import vault.zip as arch

import functionalities.add as func_add
import functionalities.consult as func_consult
import functionalities.delete as func_del
import functionalities.generate as func_gen
import functionalities.modify as func_modify

from kivy.core.window import Window

from kivy.metrics import dp, sp

from kivy.properties import StringProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.uix.scrollview import ScrollView


from kivymd.app import MDApp

from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import (
    MDIconButton,
    MDRectangleFlatButton,
    MDRectangleFlatIconButton,
    MDTextButton
)
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen


VAULT = Vault("try", "try")
Window.size = (400, 700)


class LoginScreen(MDScreen):
    def on_click(self, login, pwd):
        VAULT = Vault(login, pwd)
        # arch.undo_zip(vault)
        self.manager.transition.direction = "left"
        self.manager.current = "app"

    def clear(self):
        self.ids.login.text = ""
        self.ids.pwd.text = ""

class MD3Card(MDCard):
    pass


class AppScreen(MDScreen):
    pwd = StringProperty("")

    def __init__(self, **kwargs):
        self.custom_list = func_gen.ALPHABET
        self.account_list = {}
        self.test_list = ["test.csv", "test2.csv", "test3.csv"]
        self.scroll = ScrollView()
        self.layout = GridLayout()
        super(AppScreen, self).__init__(**kwargs)

    card_url = StringProperty("test.com")
    card_name = StringProperty("test")
    card_login = StringProperty("test")
    card_pwd= StringProperty("test")

    def add_digits_to_list(self, widget):
        if widget.active and widget.name == "digits":
            self.custom_list += func_gen.DIGIT
        else:
            self.custom_list = [x for x in self.custom_list if x not in func_gen.DIGIT]

    def add_spec_to_list(self, widget):
        if widget.active and widget.name == "spec_char":
            self.custom_list += func_gen.SPEC_CHARS
        else:
            self.custom_list = [
                x for x in self.custom_list if x not in func_gen.SPEC_CHARS
            ]

    def do_generate(self, widget):
        self.pwd = func_gen.generate(widget.value, self.custom_list)
        return self.pwd

    def save(self, **kwargs):
        #arch.save(VAULT)
        self.manager.transition.direction = "right"
        self.manager.current = "login"

    def change_card_items(self, carousel):
        print(self.ids)
        print("carousel", carousel.ids)

    def consult(self, *args):
        print("consult")

    def remove(self, *args):
        print("remove")

    def refresh(self, *args):
        print("refresh")


class ConsultScreen(MDScreen):
    def __init__(self, **kwargs):
        self.account_list = {}
        self.test_list = ["test.csv", "test2.csv", "test3.csv"]
        self.layout = GridLayout()
        super(ConsultScreen, self).__init__(**kwargs)

    def get_list_account(self, *args):
        main_box = self.ids.consult_grid
        main_box.clear_widgets()
        self.scroll = ScrollView(
            size_hint=(1, None), size=(Window.width, Window.height * 5 / 7)
        )
        self.layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.layout.bind(minimum_height=self.layout.setter("height"))


        # for file in VAULT.content:
        for file in self.test_list:
            text_button = file.strip(".csv")
            # account = func_consult.get_account(file, VAULT, "r")
            account = Account(text_button, "test", "test", "test.com")
            account_button = MDRectangleFlatButton(
                id=text_button,
                text=text_button,
                font_size=sp(12),
                padding=(0, dp(5)),
                size_hint=(0.8, None),
                height=dp(30),
                pos_hint={"center_x": 0, "center_y": 0.5},
            )

            trash_id = text_button + "_trash"
            trash_icon = MDIconButton(
                id=trash_id,
                icon="delete-outline",
                size_hint=(0.10, 0.8),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
            trash_icon.bind(on_press=self.remove)

            refresh_id = text_button + "_refresh"
            refresh_icon = MDIconButton(
                id=refresh_id,
                icon="refresh",
                size_hint=(0.10, 0.8),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
            refresh_icon.bind(on_press=self.refresh)

            self.layout.add_widget(trash_icon)
            self.layout.add_widget(refresh_icon)
            self.layout.add_widget(account_button)

            account.widgets["trash"] = trash_icon
            account.widgets["refresh"] = refresh_icon
            account.widgets["button"] = account_button
            self.account_list[text_button] = account

        self.scroll.add_widget(self.layout)
        main_box.add_widget(self.scroll)

    def remove(self, instance):
        account_name, icon = str(instance.id).split("_")
        if account_name in self.account_list.keys():
            current_account = self.account_list[account_name]
            trash = current_account.widgets.get("trash")
            self.layout.remove_widget(trash)
            refresh = current_account.widgets.get("refresh")
            self.layout.remove_widget(refresh)
            acnt_button = current_account.widgets.get("button")
            self.layout.remove_widget(acnt_button)
            filename = account_name + ".csv"
            # func_del.remove_file(file=filename, vault=VAULT)
            self.account_list.pop(account_name)
            # VAULT.content.pop(filename)
            self.test_list.pop(self.test_list.index(filename))

    def refresh(self, instance):
        filename = str(instance.id).replace("_refresh", ".csv")
        # if filename in VAULT.content:
        if filename in self.test_list:
            main_box = self.ids.consult_grid
            main_box.clear_widgets()
            text_button = filename.strip(".csv")
            # account = func_consult.get_account(filename, VAULT, "r")
            account = Account(text_button, "test", "test", "test.com")
            inside_grid = GridLayout(cols=2)
            for field in ["Name", "Login", "Password", "Url"]:
                current_label_id = field.lower() + "_label"
                label = MDLabel(id=current_label_id, text=field)
                current_txtfield_id = field.lower() + "_txtfield"
                if field == "Name":
                    textfield = MDTextField(hint_text=account.name)
                    account.txt_widgets["name"] = textfield
                elif field == "Login":
                    textfield = MDTextField(hint_text=account.login)
                    account.txt_widgets["login"] = textfield
                elif field == "Password":
                    textfield = MDTextField(hint_text="", password=True)
                    account.txt_widgets["pwd"] = textfield
                else:
                    textfield = MDTextField(hint_text=account.url)
                    account.txt_widgets["url"] = textfield
                inside_grid.add_widget(label)
                inside_grid.add_widget(textfield)
            main_box.add_widget(inside_grid)
            inner_box = BoxLayout(padding=(0, dp(20)), spacing=dp(20))
            back_button = MDRectangleFlatIconButton(text="Back", icon="arrow-left")
            back_button.bind(on_press=self.get_list_account)
            button_text = f"Update {account.name} in Vault"
            update_button = MDRectangleFlatIconButton(
                text=button_text, icon="archive-edit-outline",
                pos_hint={"center_x": self.width/2}
            )
            update_button.bind(on_press=self.update_account)
            inner_box.add_widget(back_button)
            inner_box.add_widget(update_button)
            main_box.add_widget(inner_box)

    def update_account(self, instance):
        text = str(instance.text).split(" ")
        filename = text[1] + ".csv"
        # account = func_consult.get_account(filename, VAULT, "r")
        # in_label = func_modify.do_modifying_interface(VAULT, account)
        in_label = f"{str(instance.text)} was modified in your Vault"
        main_box = self.ids.consult_box
        result_label = MDLabel(text=in_label)
        main_box.add_widget(result_label)


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
            self.custom_list = [
                x for x in self.custom_list if x not in func_gen.SPEC_CHARS
            ]

    def do_generate(self, widget):
        self.pwd = func_gen.generate(widget.value, self.custom_list)
        return self.pwd


class AddScreen(MDScreen):
    pass


class VaultApp(MDApp):
    def build(self):
        self.title = "[Vault App] by Cabron"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(GenerateScreen(name="generate"))
        sm.add_widget(AddScreen(name="add"))
        sm.add_widget(ConsultScreen(name="consult"))
        sm.add_widget(AppScreen(name="app"))
        return sm

    def change_screen(self, **kwargs):
        print(kwargs["screen"].name)
        if "Logout" in kwargs["widget"].text:
            # arch.save(VAULT)
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
