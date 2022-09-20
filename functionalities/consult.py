import csv

import crypt.decrypt as crypt

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
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                row = crypt.decrypt(vault, row)
                print(row)
                if research in row:
                    account, login, password, url = row.split("|")
                    return account, login, password, url
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
