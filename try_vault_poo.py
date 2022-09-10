import getpass


class Vault:
    def __init__ (self, login, password):
        self.login = login
        self.password = password
        self.file = f"{login}.csv"
        self.archive = f"{login}.zip"

    @property
    def get_login(self):
        return self.login

    @login.setter
    def login(self, login):
        if not login:
            login = getpass.getuser()
        self._login = login

    @property
    def get_password(self):
        return self.password

    @password.setter
    def password(self, password):
        if not password:
            password = getpass.getpass()
        self._password = password

    @property
    def get_file(self):
        return self.file

    @property:
    def get_archive(self):
        return self.archive
        