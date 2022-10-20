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
        """
        Add the DIGITS list to the custom_list for creating a password

        Parameters:
        -----------------
        login: MDTextField
        pwd: ClickableTextFieldRound object

        Returns:
        -----------------

        """
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
        """
        Clear MDTextField

        Parameters:
        -----------------


        Returns:
        -----------------

        """
        
        self.ids.login.text = ""
        self.ids.pwd.text = ""


class ClickableTextFieldRound(MDRelativeLayout):
    """
    text field composed with a MDTextField an MDIconButton
    to reveal the password
    """
    text = StringProperty()
    hint_text = StringProperty("Password")


class ClickableTextFieldLine(MDRelativeLayout):
    """
    text field composed with a MDTextField an MDIconButton
    to reveal the password
    """
    text = StringProperty()
    hint_text = StringProperty("Password")


class AppScreen(MDScreen):
    pwd = StringProperty("")

    def __init__(self, **kwargs):
        self.custom_list = func_gen.ALPHABET
        self.account_list = {}
        super(AppScreen, self).__init__(**kwargs)

    def add_digits_to_list(self, widget):
        """
        Add the DIGITS list to the custom_list for creating a password

        Parameters:
        -----------------
        widget: MDSwitch

        Returns:
        -----------------

        """
        if widget.active and widget.name == "digits":
            self.custom_list += func_gen.DIGIT
        else:
            self.custom_list = [x for x in self.custom_list if x not in func_gen.DIGIT]

    def add_spec_to_list(self, widget):
        """
        Add the SPEC_CHARS list to the custom_list for creating a password

        Parameters:
        -----------------
        widget: MDSwitch

        Returns:
        -----------------

        """
        if widget.active and widget.name == "spec_char":
            self.custom_list += func_gen.SPEC_CHARS
        else:
            self.custom_list = [
                x for x in self.custom_list if x not in func_gen.SPEC_CHARS
            ]

    def do_generate(self, widget):
        """
        Generate a password with generate() in ./functionalities/generate.py

        Parameters:
        -----------------
        widget: MDSlider

        Returns:
        -----------------
        pwd: str
        """
        self.pwd = func_gen.generate(widget.value, self.custom_list)
        return self.pwd


    def generate_consult(self, *args):
        """
        Create a GridLayout of 2 x 2 MDRaisedButton each representing an account
        and add each grid in the Carousel

        Parameters:
        -----------------
        vault: Vault object from class_vault.py

        Returns:
        -----------------

        """
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
        """
        Create a button with the name of the account

        Parameters:
        -----------------
        account: Account

        Returns:
        -----------------
        button: MDRaisedButton
            representing an account
        """
        button = MDRaisedButton(
            text=account.name, size_hint=(self.width / 3 - dp(10), dp(60))
        )
        button.bind(on_press=self.consult)
        return button

    def consult(self, *args):
        """
        Search if the text of the button exist in vault.content,
        if it's ok, generate an AccountScreen, add it to the ScreenManager,
        and change to the AccountScreen

        Parameters:
        -----------------
        args: list

        Returns:
        -----------------

        """
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
        """
        Search if an account exist in vault.content

        Parameters:
        -----------------
        widget: MDTextField

        Returns:
        -----------------

        """
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
        """
        Adding an account in vault 

        Parameters:
        -----------------
        name_wdgt: MDTextField
        login_wdgt: MDTextField
        pwd_wdgt: MDTextField
        url_wdgt: MDTextField

        Returns:
        -----------------

        """
        account = Account(name_wdgt.text, login_wdgt.text, pwd_wdgt.text, url_wdgt.text)
        label_text = func_add.add_interface(self.manager.get_screen("login").vault, account)
        self.ids.label_inner_add.text = label_text
        pass


class AccountScreen(MDScreen):
    def __init__(self, **kwargs):
        super(AccountScreen, self).__init__(**kwargs)

    def define_account(self, account: Account, widget):
        """
        Get the account and the corresponding button in AppScreen

        Parameters:
        -----------------
        account: Account object
        widget: MDButton

        Returns:
        -----------------

        """
        self.account = account
        self.widget = widget

    def on_enter(self, *args):
        """
        Insert account's settings in the corresponding TextField

        Parameters:
        -----------------

        Returns:
        -----------------

        """
        self.ids.account_name_field.text = self.account.name
        self.ids.login_field.text = self.account.login
        self.ids.url_field.text = self.account.url
        self.ids.pwd_field.children[1].text = self.account.pwd

    def remove(self, *args):
        """
        Delete an account in a vault 

        Parameters:
        -----------------

        Returns:
        -----------------

        """
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
        """
        Change parameters of the account when the user want to modify them

        Parameters:
        -----------------

        Returns:
        -----------------

        """
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

    def change_screen(self, *args):
        """
        Change the screen in the MDApp

        Parameters:
        -----------------
        args: list of arguments
            args allow to search if a screen is in ScreenManager

        Returns:
        -----------------

        """
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
        """
        Create the MDApp with title and themes.
        Adding some Screens to ScreenManager sm

        Parameters:
        -----------------

        Returns:
        -----------------

        """
        self.title = "[Vault App] by Cabron"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(AppScreen(name="app"))
        return sm

    def on_stop(self):
        """
        When the user close the window, execute save()

        Parameters:
        -----------------

        Returns:
        -----------------
        
        """
        self.save()

    def save(self):
        """
        Execute the save() function in /vault/zip.py and change the screen to LoginScreen
        if the user have clicked on logout tab

        Parameters:
        -----------------

        Returns:
        -----------------

        """
        arch.save(sm.get_screen("login").vault)
        sm.transition.direction = "right"
        sm.current = "login"
        sm.get_screen("login").clear()
        

def run():
    VaultApp().run()
