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
            f"Your login for {account.name} is {account.login}\n"+
            f"the password associated is {account.pwd}\n"+
            f"on {formate_url(account.url)}"
        )
    return (
        f"Your login for {account.name} is {account.login}\nthe password associated is {account.pwd}\n"
    )
    

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
    except EOFError:
        raise EOFError

    research = research.lower().strip()
    account_file = research + ".csv"
    print(os.getcwd(), f"\n{account_file}")
    if account_file in vault.content:
        with open(account_file, mode) as f:
            data = crypt.get_decrypt_data(vault, f)
            print(data)
            name = data["ciphertext"]["account"]
            login = data["ciphertext"]["login"]
            password = data["ciphertext"]["pwd"]
            url = data["ciphertext"]["url"]
            find_account = account.Account(name, login, password, url)
            if find_account:
                print("account was found")
                return find_account
            else:
                raise EOFError
    else:
        return funct_add.not_existing(vault)

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