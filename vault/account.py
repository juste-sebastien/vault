import getpass
import os

import vault.vault as vault

import functionalities.consult as consult


class Account:
    def __init__(self, name, login, password, url):
        self.name = name
        self.login = login
        self.pwd = password
        self.url = url
        self.file = f"{self.name}.csv"
        self.setting = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, login):
        self._login = login

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, password):
        self._pwd = password

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        if not url:
            self._url = "No registered URL"
        else:
            formated_url = consult.formate_url(url)
            self._url = formated_url

    @property
    def setting(self):
        return self._setting

    @setting.setter
    def setting(self, settings):
        self._setting = settings

    @classmethod
    def get(cls):
        name = input("Account name: ").lower().strip()
        login = input("Login: ").lower().strip()
        password = getpass.getpass()
        try:
            url = input("Url: ")
            if url == "":
                raise TypeError
        except TypeError:
            url = "No url registered"
        finally:
            return Account(name, login, password, url)

    def is_existing_file(self):
        if os.path.exists(self.file):
            return True
        else:
            return False
