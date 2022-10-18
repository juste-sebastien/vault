import getpass
import os


class Vault:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.archive = f"{login}_vault.zip"
        self.temp = ""
        self.parent = self.findfile(self.archive, "/")
        self.path = self.parent + self.archive
        self.content = ""
        self.accounts_widgets = {}

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, login):
        self._login = login

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, temp_dir):
        self._temp = temp_dir

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, list_file):
        self._content = list_file

    @classmethod
    def get(cls):
        login = input("Login: ").lower().strip()
        password = getpass.getpass()
        return Vault(login, password)

    def findfile(self, name, path):
        for dirpath, dirname, filename in os.walk(path):
            if name in filename:
                return f"{dirpath}/"
