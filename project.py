import os
import csv
import random

import classes.vault as vlt
import archive.zip as arch

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
        arch.undo_zip(archive, password)
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
                        print("\nAmazing, let me create a new PWD for you")
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
    if not arch.check_existance(vault.archive):
        answer_create = input(
            f"\n {vault.login} does not exist. Do you want to create it? (yes or no) "
        ).lower().strip()
        if answer_create == "yes":
            arch.zip.create(vault, "w")
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
    choice = input("\nWhat do you want to do? ").lower().strip()
    if not choice in ["consult", "add", "generate", "usage", "quit"]:
        return "usage"
    return choice
    

def consult(mode, vault):
    """
    Open personal vault decrypt it if password correspond to the archive where encrypt with
    Print login and password for a specified account register in the vault

    Parameters:
    -----------------
    vault: vault object
    mode: str
        "mode" to give the parameter of open() r for reading and w for writing

    Returns:
    -----------------
    f-str: str
        A formatted string with account, login, password and if exist url

    """
    try: 
        search_return = search(mode, vault)
    except EOFError:
        raise EOFError
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    try:
        account, acnt_login, acnt_pwd, acnt_url = search_return
    except TypeError:
            raise TypeError
    except ValueError:
        raise ValueError
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
    No return
    
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
    numbers, and all specials characters excluded " ' ` and ,

    Parameters:
    -----------------
        

    Returns:
    -----------------
    pwd_created: str
        "pwd_created" is a random password created for the user
    """
    try:
        pwd_length = int(
            input("Which length do you want for your Password? ")
        )
    except ValueError:
        print("You need to type an integer\n")
        raise ValueError
    except TypeError:
        print("You need to type an integer\n")
        raise TypeError
    else:
        pwd_created = ""
        i = 0
        while i < pwd_length:
            char = random.randint(32, 127)
            if chr(char) in ['"', "'", "`", ","]:
                pass
            else:
                pwd_created += chr(char)
                i += 1
        return pwd_created


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
    row[""]: tuple
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


def formate_url(url):
    """
    Formate an url "google.com" to the format "http://wwww.google.com"

    Parameters:
    -----------------
    url: str
        give by user when he add an account
    
    Returns:
    -----------------
    f-string: str
        a formatted string like "http://www.google.com"
    """
    http = ""
    www = ""
    if ("http://" or "https://") in url:
        http, url = url.split("http://")
    if "www." in url:
        www, url = url.split("www.")
    if http == "" or www == "":
        url = f"http://www.{url}"
        return url
    return f"{http}{www}{url}"


def save(vault):
    """
    Call do_zip() to compress the archive and remove csv fil

    Parameters:
    -----------------
    vault: a Vault object

    Returns:
    -----------------
    str
        a comment to close Vault app and granted user
    """
    arch.do_zip(vault.archive, vault.file, vault.password)
    if os.path.exists(vault.file):
        os.remove(vault.file)
    return "\n Thank's for using Vault"


if __name__ == "__main__":
    main()
