import os

import crypt.decrypt as crypt

from vault.zip import check_existance
import vault.account as account
import functionalities.add as funct_add


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
    prompt = "For which account do you want get the password? "
    try:
        account = search(mode, vault, prompt)
    except EOFError:
        raise EOFError
    except KeyboardInterrupt:
        raise KeyboardInterrupt

    if not "No url" in account.url:
        return (
            f"Your login for {account.name} is {account.login}\n"
            + f"the password associated is {account.pwd}\n"
            + f"on {formate_url(account.url)}"
        )
    return f"Your login for {account.name} is {account.login}\nthe password associated is {account.pwd}\n"


def search(mode, vault, prompt):
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
    data[""]: tuple
        only if a corresponding data was found
    """
    try:
        research = input(prompt).lower().strip()
        if "quit" in research:
            raise KeyboardInterrupt
    except Exception:
        raise KeyboardInterrupt

    research = research.lower().strip()
    account_file = research + ".csv"
    if account_file in vault.content:
        with open(account_file, mode) as f:
            data = crypt.get_decrypt_data(vault, f)
            print(data)
            name = data["ciphertext"]["account"]
            login = data["ciphertext"]["login"]
            password = data["ciphertext"]["pwd"]
            url = data["ciphertext"]["url"]
            return account.Account(name, login, password, url)
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
    http = "http"
    www = "www"
    if "http://" in url:
        http, url = url.split("://")
    elif "https://" in url:
        http, url = url.split("://")

    if "www." in url:
        url = url.split(".", maxsplit=1)
    return f"{http}://{www}.{url}"
