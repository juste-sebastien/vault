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

    @classmethod
    def get(cls):
        """
        Prompt user to create a vault

        Parameters:
        -----------------

        Returns:
        -----------------
        Vault: Vault object
        """
        login = input("Login: ").lower().strip()
        password = getpass.getpass()
        return Vault(login, password)


    def findfile(self, name, path):
        """
        Search a specific file in all the os 

        Parameters:
        -----------------
        name: str
            representing a file name
        path: str
            path of the file

        Returns:
        -----------------
        f-string: str
            complete path of file
        """
        for dirpath, dirname, filename in os.walk(path):
            if name in filename:
                return f"{dirpath}/"
