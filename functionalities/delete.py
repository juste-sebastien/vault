import os

import functionalities.add as funct_add


def delete_account(vault):
    """
    Prompt user to define the account to delete, call remove_file. If True
    return a f-string to confirm the removing else call not_existing()
    in ./functionalities/add.py

    Parameters:
    -----------------
    account: Account object
    parameter: str

    Returns:
    -----------------
    f-string: str
    or 
    not_existing(): function

    """
    account_name = str(input("Which account do you want to delete? ")).strip().lower()
    if "quit" in account_name:
        raise KeyboardInterrupt
    account_file = account_name + ".csv"
    if account_file in vault.content:
        if remove_file(account_file, vault):
            return f"{account_name} was deleted from your Vault"
    else:
        return funct_add.not_existing(vault)


def remove_file(file, vault):
    """
    Boolean function that check if the file exist and remove it

    Parameters:
    -----------------
    file: str
        representing a file account
    vault: Vault object

    Returns:
    -----------------
    True or False

    """
    os.remove(file)
    vault.content = os.listdir()
    if os.path.exists(file):
        return False
    return True
