import os

import json
import csv

import vault.account as vlt_acnt

import crypt.encrypt as encrypt


def add(vault):
    """
    Create a new account on the csv file representing the vault

    Parameters:
    -----------------
    vault: Vault object

    Returns:
    -----------------
    add_interface(): function

    """
    account = vlt_acnt.Account.get()
    return add_interface(vault, account)


def add_interface(vault, account):
    """
    Second part of add() to match with the interface and create an account

    Parameters:
    -----------------
    account: Account object
    vault: Vault object

    Returns:
    -----------------
    save_file(): function

    """
    text = {
        "account": account.name,
        "login": account.login,
        "pwd": account.pwd,
        "url": account.url,
    }
    row = {"nonce": "", "header": "", "ciphertext": text, "tag": ""}
    account.setting = row
    
    return save_file(account, vault, "w", "added")


def not_existing(vault):
    """
    Prompt user to know if he want to add the account that not existing

    Parameters:
    -----------------
    vault: Vault Object

    Returns:
    -----------------
    add(): function

    Exceptions:
    -----------------
    KeyboardInterrupt: 
        to stop the program

    """
    print("Account seems not to be save in your Vault.")
    want_add = input("Do you want to add it in your Vault? (yes or no) ")
    if "yes" in want_add:
        return add(vault)
    else:
        raise KeyboardInterrupt


def save_file(account, vault, mode, operation):
    """
    open the corresponding file, crypt the content and add it to vault.content

    Parameters:
    -----------------
    account: Account object
    vault: Vault object
    mode: str
        corresponding to the open() mode
    operation: str

    Returns:
    -----------------
    f-string: str

    """
    acnt_filepath = vault.temp + account.file
    with open(acnt_filepath, mode) as file:
        ciphertext = encrypt.encrypt(vault, account.setting)
        set_in_csv = json.loads(ciphertext)
        col_a = set_in_csv["nonce"]
        col_b = set_in_csv["header"]
        col_c = set_in_csv["ciphertext"]
        col_d = set_in_csv["tag"]
        fieldnames = ["col a", "col b", "col c", "col d"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(
            {"col a": col_a, "col b": col_b, "col c": col_c, "col d": col_d}
        )
    if operation == "added":
        vault.content = os.listdir()
    return f"{account.name} had been {operation} to your Vault"
