import getpass


class Account:
    def __init__(self, name, login, password, url):
        self.name = name
        self.login = login
        self.pwd = password
        self.url = url
        self.file = f"{self.name}.csv"
        self.setting = {}
        self.widget = ""


    @classmethod
    def get(cls):
        """"
        Prompt user to an account in vault
        User could choose between consult, add, generate, usage and quit
        if not, generate returns usage

        Parameters:
        -----------------

        Returns:
        -----------------
        Account object
        """
        name = input("Account name: ").lower().strip()
        login = input("Login: ").lower().strip()
        password = getpass.getpass()
        try:
            url = input("Url: ")
            if url == "":
                raise TypeError
        except TypeError:
            url = ""
        finally:
            return Account(name, login, password, url)
