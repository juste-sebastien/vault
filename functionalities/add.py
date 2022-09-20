import csv
import crypt.encrypt as crypt

def add(vault, file, mode):
    """
    Add a new account on the csv file representing the vault

    Parameters:
    -----------------
    file: str
        A "file" str is returned by calling vault.file
    mode: str
        "mode" to give the parameter of open() a for append to the current vault

    Returns:
    -----------------
    No return
    
    """
    with open(file, mode) as f:
        writer = csv.writer(f, delimiter=",")
        account = input("Account Name: ").lower().strip()
        login = input("Login: ").strip()
        pwd = input("Password: ").strip()
        try:
            url = input("Url: ")
            if url == "":
                raise TypeError
        except TypeError:
            url = "No url registered"
        row = f"{account}|{login}|{pwd}|{url}"
        writer.writerow(
            crypt.encrypt(vault, row)
        )


