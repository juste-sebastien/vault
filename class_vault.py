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

    @property
    def get_password(self):
        return self.password

    @classmethod
    def get(cls):
        login = input("Login: ").lower().strip()
        password = getpass.getpass()
        return Vault(login, password)


def main():
    vault = Vault.get()
    print(vault.file, vault.archive)


if __name__ == "__main__":
    main()