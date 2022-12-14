import getpass
import os

import functionalities.add as funct_add

import functionalities.consult as funct_consult


def do_modifying(vault):
    """
    Prompt user for the account to change, and the parameter

    Parameters:
    -----------------
    vault: Vault Object

    Returns:
    -----------------
    do_modifying_interface(): function
    or
    str

    """
    prompt = "Which account do you want modify? "
    try:
        account = funct_consult.search("r", vault, prompt)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except EOFError:
        raise EOFError

    parameter = get_parameter()

    if change_set(account, parameter):
        return do_modifying_interface(vault, account)
    else:
        return "Sorry, we can't modifying your account"


def do_modifying_interface(vault, account):
    """
    Get the account settings, put them in a dict, update account.setting dict,
    remove the corresponding file and save it by calling save_file()
    in ./functionalities/add.py

    Parameters:
    -----------------
    account: Account object
    vault: Vault object

    Returns:
    -----------------
    save_file(): function in ./functionalities/add.py

    """
    text = {
        "account": account.name,
        "login": account.login,
        "pwd": account.pwd,
        "url": account.url,
    }
    row = {"nonce": "", "header": "", "ciphertext": text, "tag": ""}
    account.setting = row
    os.remove(account.file)
    return funct_add.save_file(account, vault, "w", "modified")


def get_parameter():
    """
    Prompts user to get the parameter of the account to change
    Parameters:
    -----------------

    Returns:
    -----------------
    parameter: str
    or
    get_parameter()

    """
    try:
        parameter = str(input("Which parameter do you want to change? "))
    except:
        print("I'm sorry, but i've don't understand what you want. Please try again.")
        return get_parameter()
    else:
        if parameter in ["name", "n", "login", "l", "password", "p", "pwd", "url", "u"]:
            return parameter
        else:
            print("Options: name or n\n\t\tlogin or l\n\t\tpassword or p\n\t\turl or u")
            return get_parameter()


def change_set(account, parameter):
    """
    Boolean function that check the parameter of the account to change, 
    prompt user for the new one and update the account setting

    Parameters:
    -----------------
    account: Account object
    parameter: str

    Returns:
    -----------------
    True or False

    """
    if parameter in ["name", "n"]:
        account.name = str(input("New account name: "))
        return True
    elif parameter in ["login", "l"]:
        account.login = str(input("New account login: "))
        return True
    elif parameter in ["password", "pwd", "p"]:
        account.pwd = getpass.getpass()
        return True
    elif parameter in ["url", "u"]:
        account.url = str(input("New account name: "))
        return True
    else:
        return False
