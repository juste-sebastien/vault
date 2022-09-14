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
    try:
        vault = get_welcome()
    except TypeError:
        pass
    else:
        file = vault.file
        archive = vault.archive
        password = vault.password
        path_file = "./" + file
        undo_zip(archive, password)
        while True:
            try:
                choice = get_choice()
                if "quit" in choice:
                    raise KeyboardInterrupt
                elif not choice.isalpha():
                    raise TypeError
            except KeyboardInterrupt:
                break
            except TypeError:
                print(f"{USAGE}")
                pass
            except EOFError:
                break
            else:
                match choice:
                    case "consult":
                        print(f"\nGroovy we're gonna to consult your vault")
                        mode = "r"
                        try:
                            account = consult(mode, vault)
                        except KeyboardInterrupt:
                            break
                        except EOFError:
                            print("Account seems not to be save in your Vault.")
                            want_add = input("Do you want to add it in your Vault? (yes or no) ")
                            if "yes" in want_add:
                                add(vault.file, "a+")
                            else:
                                pass
                        except TypeError:
                            pass
                        else:
                            print(account)


                    case "add":
                        print("\nLet's go for adding a new set in to your vault")
                        mode = "a"
                        add(file, mode)

                    case "generate":
                        try:
                            pwd = generate()
                        except ValueError:
                            generate()
                        except TypeError:
                            generate()
                        else:
                            print(pwd)

                    case "usage":
                        print(f"{USAGE}")
                    case _:
                        pass
    print(save(vault))


def get_welcome():
    """
    Print usage of the app and create a vault object. If the vault not exist,
    a new vault is created by calling create().

    Parameters:
    -----------------
        None

    Returns:
    -----------------
        vault:
            a vault object
    """
    print("Welcome in Vault App.\n" + f"{USAGE}\n")
    vault = vlt.Vault.get()
    if not check_existance(vault.archive):
        answer_create = input(
            f"\n {vault.login} does not exist. Do you want to create it? (yes or no) "
        ).lower().strip()
        if answer_create == "yes":
            create(vault, "w")
        else:
            raise TypeError
    return vault


def get_choice():
    """
    
    Prompt user to make a choice for using vault
    User could choose between consult, add, generate, usage and quit 
    if not, function returns usage

    Parameters:
    -----------------
        vault: Vault object from class_vault.py

    Returns:
    -----------------
        choice
    """
    choice = input("What do you want to do? ").lower().strip()
    if not choice in ["consult", "add", "generate", "usage", "quit"]:
        return "usage"
    return choice
    

def consult(mode, vault):
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
        account, acnt_login, acnt_pwd, acnt_url = search(mode, vault)
    except TypeError:
            raise TypeError
    except ValueError:
        raise ValueError
    except EOFError:
        raise EOFError
    except KeyboardInterrupt:
        raise KeyboardInterrupt

    else:
        if not "No url" in acnt_url:
            return (
                f"Your login for {account} is {acnt_login}\n"+
                f"the password associated is {acnt_pwd}\n"+
                f"on {formate_url(acnt_url)}"
            )
        return (
            f"Your login for {account} is {acnt_login}\nthe password associated is {acnt_pwd}\n"
        )


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
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=",")
        account = input("Account Name: ").lower().strip()
        login = input("Login: ").strip()
        pwd = input("Password: ").strip()
        try:
            url = input("Url: ")
            if url == "":
                raise TypeError
        except TypeError:
            url = "No url registered"
        writer.writerow(
            {"account": account, "login": login, "password": pwd, "url": url}
        )


def generate():
    """
    Generate a random password from the ASCII table, including lower and uppercase,
    numbers, and all specials characters

    Parameters:
    -----------------
        

    Returns:
    -----------------
        pwd_created: str
            "pwd_created" is a random password created for the user
    """
    print(f"Amazing, let me create a new PWD for you")
    try:
        pwd_length = int(
            input("Which length do you want for your Password? ")
        )
    except ValueError:
        print("You need to type an integer\n")
        return ValueError
    except TypeError:
        print("You need to type an integer\n")
        return TypeError
    else:
        pwd_created = ""
        for _ in range(pwd_length):
            char = random.randint(32, 127)
            if chr(char) in ['"', "'", "`", ","]:
                pass
            else:
                pwd_created += chr(char)
        return f"{generate(pwd_length)}\n"


def check_existance(archive):
    """
    Check if the file exist in the current folder
    
    Parameters:
    -----------------
    archive: str
        "archive" str returned by calling vault.archive

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
    if os.path.exists(archive):
        return True
    else:
        return False


def search(mode, vault):
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
    try:
        research = input("For which account do you want get the password? ").lower().strip()
        if "quit" in research:
            raise KeyboardInterrupt
    except EOFError:
        raise EOFError
    else:
        research = research.lower().strip()
        with open(vault.file, mode) as f:
            fieldnames = ["account", "login", "password", "url"]
            reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=",")
            for row in reader:
                if row["account"] == research:
                    return row["account"], row["login"], row["password"], row["url"]
            raise EOFError


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
    pyminizip.uncompress(archive, pwd, "./", 5)


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
    pyminizip.compress(file, None, archive, pwd, 5)


def formate_url(url):
    if ("http://" or "https://") in url:
        pass
    elif "www." in url:
        pass
    else:
        url = f"http://www.{url}"
    return url



def save(vault):
    do_zip(vault.archive, vault.file, vault.password)
    if os.path.exists(vault.file):
        os.remove(vault.file)
    return "\n Thank's for using Vault"


if __name__ == "__main__":
    main()
