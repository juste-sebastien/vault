import os

from vault.account import Account
import vault.vault as vlt
import vault.zip as arch

import functionalities.add as func_add
import functionalities.consult as func_consult
import functionalities.delete as func_del
import functionalities.generate as func_gen
import functionalities.modify as func_modify

from functools import partial

from kivy.clock import Clock

from kivy.core.window import Window

from kivy.metrics import dp, sp

from kivy.properties import StringProperty

from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen

current_account = ""
Window.size = (400, 700)


class LoginScreen(MDScreen):
    def on_click(self, login, pwd):
        self.vault = vlt.Vault(login.text, pwd.ids.pwd_text_field.text)
        if self.vault.login != "" and self.vault.password != "":
            arch.undo_zip(self.vault)
            self.manager.transition.direction = "left"
            self.manager.current = "app"
        else:
            self.ids.login.error = True
            self.ids.login.helper_text = "Login is required"
            self.ids.pwd.ids.pwd_text_field.error = True
            self.ids.pwd.ids.pwd_text_field.helper_text = "Password is required"

    def clear(self):
        self.ids.login.text = ""
        self.ids.pwd.text = ""


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty("Password")


class ClickableTextFieldLine(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty("Password")


class AppScreen(MDScreen):
    pwd = StringProperty("")

    def __init__(self, **kwargs):
        self.custom_list = func_gen.ALPHABET
        self.account_list = {}
        super(AppScreen, self).__init__(**kwargs)

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


    def generate_consult(self, *args):
        carousel = self.ids.carousel_card
        carousel.clear_widgets()
        temp_list = self.manager.get_screen("login").vault.content
        grid_range = len(temp_list) / 4
        if int(grid_range) < grid_range:
            grid_range = int(grid_range) + 1
        else:
            grid_range = int(grid_range)
        i = 0
        for _ in range(grid_range):
            grid = GridLayout(
                cols=2,
                spacing=dp(10),
                padding=dp(20),
                row_force_default=True,
                row_default_height=carousel.height / 4,
            )
            for _ in range(4):
                if i >= len(temp_list):
                    break
                account = func_consult.get_account(
                    temp_list[i], self.manager.get_screen("login").vault, "r"
                )
                account_card = self.generate_card(account)
                account.widget = account_card
                grid.add_widget(account_card)
                self.manager.get_screen("login").vault.accounts_widgets[
                    account.name
                ] = {"account": account, "widget": account_card}
                i += 1
            carousel.add_widget(grid)

    def generate_card(self, account: Account):
        button = MDRaisedButton(
            text=account.name, size_hint=(self.width / 3 - dp(10), dp(60))
        )
        button.bind(on_press=self.consult)
        return button

    def consult(self, *args):
        for key, value in self.manager.get_screen(
            "login"
        ).vault.accounts_widgets.items():
            if args[0].text == key:
                account = self.manager.get_screen("login").vault.accounts_widgets[
                    args[0].text
                ]["account"]
        current_account = AccountScreen(name="account")
        current_account.define_account(account, args[0])
        sm.add_widget(current_account)
        sm.transition.direction = "left"
        sm.current = "account"

    def search(self, widget):
        found = False
        for key in self.manager.get_screen("login").vault.accounts_widgets.keys():
            if widget.text == key:
                account_widget = self.manager.get_screen(
                    "login"
                ).vault.accounts_widgets[widget.text]["widget"]
                found = True
                break
        if not found:
            self.ids.research_label.text = (
                "Sorry this account seems not to be in your Vault"
            )
        else:
            self.consult(account_widget)

    def add(self, name_wdgt, login_wdgt, pwd_wdgt, url_wdgt):
        account = Account(name_wdgt.text, login_wdgt.text, pwd_wdgt.text, url_wdgt.text)
        label_text = func_add.add_interface(self.manager.get_screen("login").vault, account)
        self.ids.label_inner_add.text = label_text
        pass


class AccountScreen(MDScreen):
    def __init__(self, **kwargs):
        super(AccountScreen, self).__init__(**kwargs)

    def define_account(self, account: Account, widget):
        self.account = account
        self.widget = widget

    def on_enter(self, *args):
        self.ids.account_name_field.text = self.account.name
        self.ids.login_field.text = self.account.login
        self.ids.url_field.text = self.account.url
        self.ids.pwd_field.children[1].text = self.account.pwd

    def remove(self, *args):
        if self.widget.text in self.manager.get_screen("login").vault.accounts_widgets:
            del self.manager.get_screen("login").vault.accounts_widgets[
                self.widget.text
            ]
        self.manager.get_screen("app").ids.carousel_card.children[0].children[
            0
        ].remove_widget(self.widget)
        func_del.remove_file(
            file=self.account.file, vault=self.manager.get_screen("login").vault
        )
        self.ids.consult_label.text = f"{self.account.name} was deleted from your Vault"
        Clock.schedule_once(partial(self.change_screen, self), 2)

    def refresh(self, *args):
        self.account.name = self.ids.account_name_field.text
        self.account.login = self.ids.login_field.text
        self.account.pwd = self.ids.pwd_field.children[1].text
        self.account.url = self.ids.url_field.text

        self.manager.get_screen("login").vault.accounts_widgets[self.account.name][
            "account"
        ] = self.account
        self.ids.consult_label.text = func_modify.do_modifying_interface(
            self.manager.get_screen("login").vault, self.account
        )
        # self.ids.consult_label.text = f"{self.account.name} was modified in your Vault"

    def change_screen(self, *args):
        self.ids.consult_label.text = ""
        for i in range(len(args)):
            if args[i] in sm.screens:
                screen = args[i]
                sm.transition.direction = "right"
                sm.current = "app"
                sm.remove_widget(screen)


sm = ScreenManager()


class VaultApp(MDApp):
    def build(self):
        self.title = "[Vault App] by Cabron"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(AppScreen(name="app"))
        return sm

    def on_stop(self):
        self.save()

    def save(self):
        arch.save(sm.get_screen("login").vault)
        sm.transition.direction = "right"
        sm.current = "login"
        sm.get_screen("login").clear()
        

def run():
    VaultApp().run()
