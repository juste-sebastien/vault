import os
import csv
import random

import zipfile
import pyminizip

import class_vault as vlt

USAGE = str(
    "\n"
    + "consult -> for consulting a password in your vault\n"
    + "generate -> for generating a new password\n"
    + "add -> for adding a new account(login + password) in to your vault\n"
    + "CTRL + D or CTRL + C or quit -> to save your vault and quit program\n"
    + "usage -> when you don't know what to do"
)


def main():
    get_welcome()


def get_welcome():
    """
    Print usage of the app and create a vault object. If the vault not exist,
    a new vault is created by calling create(). Finally, get_choice() is called

    Parameters:
    -----------------
        None

    Returns:
    -----------------
        Call get_choice()
    """
    print("Welcome in Vault App.\n" + f"{USAGE}\n")
    vault = vlt.Vault.get()
    if not check_existance(vault.archive, vault.file, "r", vault.password.encode()):
        create(vault, "w")
    return get_choice(vault)


def get_choice(vault):
    """
    Extract csv from zip archive corresponding to vault
    Prompt user to make a choice for using vault

    Parameters:
    -----------------
        vault: Vault object from class_vault.py

    Returns:
    -----------------
        None
    """
    mode = "r"
    file = vault.file
    archive = vault.archive
    password = vault.password
    path_file = "./" + file
    undo_zip(archive, password)
    while True:
        try:
            choice = input("What do you want to do? ").lower().strip()
            if "quit" in choice:
                raise KeyboardInterrupt
            elif not choice.isalpha():
                raise TypeError
        except KeyboardInterrupt:
            # execute save()
            print("\nThank's for using Vault!")
            break
        except TypeError:
            print(f"{USAGE}")
            pass
        except EOFError:
            print("\nThank's for using Vault!")
            break
        else:
            match choice:
                case "consult":
                    print(f"\nGroovy we're gonna to consult your vault")
                    file = consult(file, path_file, mode)
                case "add":
                    print("\nLet's go for adding a new set in to your vault")
                    mode = "a"
                    file = add(file, mode)
                case "generate":
                    print(f"Amazing, let me create a new PWD for you")
                    try:
                        pwd_length = int(
                            input("Which length do you want for your Password? ")
                        )
                    except ValueError:
                        print("You need to type an integer\n")
                        get_choice(vault)
                    except TypeError:
                        print("You need to type an integer\n")
                        get_choice(vault)
                    else:
                        print(f"{generate(pwd_length)}\n")

                case "usage":
                    print(f"{USAGE}")
                case _:
                    pass

    do_zip(archive, file, password)
    if os.path.exists(file):
        os.remove(file)

    return None


def consult(file, path_file, mode):
    """
    Open personal vault decrypt it if password correspond to the archive where encrypt with
    Print login and password for a specified account register in the vault

    Parameters:
    -----------------
    file: str
        A "file" str is returned by calling vault.file
    pathfile: str
        "pathfile" is the name of the "file" transformed to path ./[filename]
    mode: str
        "mode" to give the parameter of open() r for reading and w for writing

    Returns:
    -----------------
        None

    """
    try:
        account, acnt_login, acnt_pwd, acnt_url = search(path_file, mode)
    except TypeError:
        print("Sorry, the account does not exist yet in your Vault")
        want_add = (
            input("Do you want to add a new account in your Vault? (yes or no) ")
            .lower()
            .strip()
        )
        if want_add == "yes":
            mode = "a"
            add(file, mode)
        else:
            consult(file, path_file, mode)
    else:
        print(
            f"Your login for {account} is {acnt_login}\nthe password associated is {acnt_pwd}\n"
        )
        return None


def add(file, mode):
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
        None
    
    """
    with open(file, mode) as f:
        fieldnames = ["account", "login", "password", "url"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="|")
        account = input("Account Name: ").lower().strip()
        login = input("Login: ").strip()
        pwd = input("Password: ").strip()
        try:
            url = input("Url: ")
        except:
            url = None
        else:
            writer.writerow(
                {"account": account, "login": login, "password": pwd, "url": url}
            )
            return None


def generate(length):
    """
    Generate a random password from the ASCII table, including lower and uppercase,
    numbers, and all specials characters

    Parameters:
    -----------------
        length: int
            "length" is given by user with a prompt

    Returns:
    -----------------
        pwd_created: str
            "pwd_created" is a random password created for the user
    """
    pwd_created = ""
    for _ in range(length):
        char = random.randint(32, 127)
        pwd_created += chr(char)
    return pwd_created


def check_existance(archive, file, mode, pwd):
    """
    Check if the file exist in the current folder
    
    Parameters:
    -----------------
    file: str
        A "file" str is returned by calling vault.file
    archive: str
        "archive" str returned by calling vault.archive
    mode: str
        "mode" to give the parameter of open() r for reading and w for writing
    pwd: getpass object
        "pwd" is a getpass object returned by calling vault.get_password()

    Returns:
    -----------------
        True
            if the file exist
        False
            if not

    Exceptions:
    -----------------
        FileNotFoundError
        IOError
    """
    try:
        with zipfile.ZipFile(archive, mode) as a:
            with a.open(file, mode, pwd) as f:
                return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False


def search(file, mode):
    """
    Search the account, login, pwd and url in the csv file

    Parameters:
    -----------------
    file: str
        A "file" str is returned by calling vault.file
    mode: str
        "mode" to give the parameter of open() r for reading and w for writing

    Returns:
    -----------------
        row[""]
            only if a corresponding row was found
    """
    research = input("\nFor which account do you want get the password? ")
    research = research.lower().strip()
    with open(file, mode) as f:
        fieldnames = ["account", "login", "password", "url"]
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter="|")
        for row in reader:
            if row["account"] == research:
                return row["account"], row["login"], row["password"], row["url"]


def create(vault, mode):
    """
    Create a new vault with an archive and a csv file 

    Parameters:
    -----------------
    vault: vault object
    mode: str
        "mode" to give the parameter of open() r for reading and w for writing

    Returns:
    -----------------
        None
    """
    with zipfile.ZipFile(vault.archive, mode) as a:
        with a.open(vault.file, mode) as f:
            return None


def undo_zip(archive, pwd):
    """
    Uncompress the archive with the associated pwd

    Parameters:
    -----------------
    archive: str
        A "archive" str is returned by calling vault.archive
    pwd: getpass object
        "pwd" is a getpass object returned by calling vault.get_password()

    Returns:
    -----------------
        None
    """
    return pyminizip.uncompress(archive, pwd, "./", 5)


def do_zip(archive, file, pwd):
    """
    Compress the archive with the associated pwd

    Parameters:
    -----------------
    archive: str
        A "archive" str is returned by calling vault.archive
    pwd: getpass object
        "pwd" is a getpass object returned by calling vault.get_password()

    Returns:
    -----------------
        None
    """
    return pyminizip.compress(file, None, archive, pwd, 5)


if __name__ == "__main__":
    main()
