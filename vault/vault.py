import getpass
import os


class Vault:
    def __init__ (self, login, password):
        self.login = login
        self.password = password
        self.archive = f"{login}.zip"
        self.temp = ""
        self.parent = f"{os.getcwd()}/"
        self.path = self.parent + self.archive

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

    @classmethod
    def get(cls):
        login = input("Login: ").lower().strip()
        password = getpass.getpass()
        return Vault(login, password)
