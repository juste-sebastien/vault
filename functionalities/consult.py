import json
import csv

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
    try: 
        current_account = search(mode, vault)
    except EOFError:
        raise EOFError
    except KeyboardInterrupt:
        raise KeyboardInterrupt

    try:
        acnt_name, acnt_login, acnt_pwd, acnt_url = current_account
    except:
        return current_account
    else:
        if not "No url" in acnt_url:
            return (
                f"Your login for {acnt_name} is {acnt_login}\n"+
                f"the password associated is {acnt_pwd}\n"+
                f"on {formate_url(acnt_url)}"
            )
        return (
            f"Your login for {acnt_name} is {acnt_login}\nthe password associated is {acnt_pwd}\n"
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
    data[""]: tuple
        only if a corresponding data was found
    """
    try:
        research = input("For which account do you want get the password? ").lower().strip()
        if "quit" in research:
            raise KeyboardInterrupt
    except EOFError:
        raise EOFError


    research = research.lower().strip()
    account_file = vault.temp + research + ".csv"
    if check_existance(account_file):
        with open(account_file, mode) as f:
            file_content = f.read()
            nonce, header, ciphertext, tag = file_content.split(",")
            content = {"nonce": nonce, "header": header, "ciphertext": ciphertext, "tag": tag}
            content = json.dumps(content)
            data = crypt.decrypt(vault, content).replace("'", '"')
            data = json.loads(data)
            if research in data["ciphertext"]["account"]:
                account = data["ciphertext"]["account"]
                login = data["ciphertext"]["login"]
                password = data["ciphertext"]["pwd"]
                url = data["ciphertext"]["url"]
                return account, login, password, url
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