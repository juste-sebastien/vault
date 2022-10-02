import os

import json
import csv

import vault.account as vlt_acnt

import crypt.encrypt as encrypt


def add(vault):
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
    f-string: str
        f-string from save_file()

    """
    account = vlt_acnt.Account.get()
    text = {
        "account": account.name,
        "login": account.login,
        "pwd": account.pwd,
        "url": account.url,
    }
    row = {"nonce": "", "header": "", "ciphertext": text, "tag": ""}
    account.setting = row
    save_file(account, vault, "w", "added")
    return account


def not_existing(vault):
    print("Account seems not to be save in your Vault.")
    want_add = input("Do you want to add it in your Vault? (yes or no) ")
    if "yes" in want_add:
        return add(vault)
    else:
        raise KeyboardInterrupt


def save_file(account, vault, mode, operation):
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
