import sys
import os
import base64

import zipfile
import getpass

import pyminizip

from cryptography.fernet import Fernet

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


USAGE = str(
    "\n"
    + "consult -> for consulting a password in your vault\n"
    + "generate -> for generating a new password\n"
    + "add -> for adding a new account(login + password) in to your vault\n"
    + "CTRL + D or CTRL + C or quit -> to save your vault and quit program\n"
)


def main():
    # get_welcome()
    get_choice()


def get_welcome():
    """print usage of the app"""


def get_choice():
    """prompt user to make a choice for using vault"""
    mode = "r"
    archive, file, password = get_filename(mode)
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
                    file = consult(file, path_file, mode)
                case "add":
                    mode = "a"
                    file = add(file, path_file, mode)
                case "generate":
                    generate()
                case "usage":
                    print(f"{USAGE}")
                case _:
                    pass
    do_zip(archive, file, password)
    if os.path.exists(file):
        os.remove(file)


def consult(file, path_file, mode):
    """open personal vault decrypt it if password correspond to hashkey"""
    print(f"\nGroovy we're gonna to consult your vault")
    try:
        account, acnt_login, acnt_pwd, acnt_url= search(path_file, mode)
    except TypeError:
        print("Sorry, the account does not exist yet in your vault")
        want_add = input("Do you want to add a new account? (yes or no) ").lower().strip()
        if want_add == "yes":
            mode = "a"
            add_with_login(file, mode)
        else:
            consult(file, path_file, mode)
    else:
        print(f"Your login for {account} is {acnt_login}\nthe password associated is {acnt_pwd}\n")
            #personal_vault = encrypt_or_decrypt(password, file, "decrypt")
    return file

def add(file, path_file, mode):
    print("\nLet's go for adding a new set in to your vault")
    return add_with_login()


def generate():
    print(f"Amazing, let me create a new pWD for you")


def get_filename(mode):
    """open the file relating to the user account"""
    account = get_login()
    pwd = get_password()
    archive = account + ".zip"
    file = account + ".csv"
    count = 0
    if check_existance(archive, file, mode):
        return archive, file, pwd
    elif count == 0:
        #if not account create, programm purpose to create one
        want_create = input("Do you want to create a new account? (yes or no) ").lower().strip()
        if want_create == "yes":
            with open(file, "w") as f:
                f.write("account, login, password, url\r\n")
            do_zip(archive, file, pwd)
            count += 1
            return archive, file, pwd
        else:
            get_filename(mode)


def check_existance(archive, file, mode):
    """check if the file exist in the current folder"""
    try:
       with zipfile.ZipFile(archive, mode) as a:
            with a.open(file, mode) as f:
                return True
    except FileNotFoundError as e:
        print(
            "Please be sure that you are in the right folder before running this script"
        )
        return False
    except IOError as e:
        print(
            "Please be sure that you are in the right folder before running this script"
        )
        return False


def encrypt_or_decrypt(pwd, file, mode):
    #todo
    bytes_pwd = bytes(pwd, "utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"",
        iterations=390000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(bytes_pwd))

    f = Fernet(key)
    token = f.encrypt(file)
    if "encrypt" in mode:
        return token.decode()
    if "decrypt" in mode:
        return f.decrypt(token).decode()


def get_login():
    return input("Login: ").lower().strip()


def get_password():
    return getpass.getpass(
        "\nPlease enter password.\n"+
        "Password: "
    )


def undo_zip(archive, pwd):
    """uncompress the archive with the associated pwd"""
    pyminizip.uncompress(archive, pwd, "./", 5)


def do_zip(archive,file, pwd):
    """compress the archive with the associated pwd"""
    pyminizip.compress(file, None, archive, pwd, 5)


def search(file, mode):
    """ search the account, login, pwd and url in the csv file"""
    research = input("\nFor which account do you want get the password? ")
    research = research.lower().strip()
    with open(file, mode) as f:
        for line in f:
            if research in line:
                account, login, pwd, url = line.split(", ", maxsplit=3)
                return account, login, pwd, url


def add_with_login(file, mode):
    with open(file, mode) as f:
        account = input("Account Name: ").lower().strip()
        login = input("Login: ").strip()
        pwd = input("Password: ").strip()
        try:
            url = input("Url: ")
        except:
            url = None
        f.write(f"{account}, {login}, {pwd}, {url}\r\n")
    return file


if __name__ == "__main__":
    main()
