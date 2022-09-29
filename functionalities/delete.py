import os

import functionalities.add as funct_add

def delete_account(vault):
    account_name = str(input("Which account do you want to delete? ")).strip().lower()
    account_file = account_name + ".csv"
    if account_file in vault.content:
        os.remove(account_file)
        vault.content = os.listdir()
        return f"{account_name} was deleted from your Vault"
    else:
        return funct_add.not_existing(vault)