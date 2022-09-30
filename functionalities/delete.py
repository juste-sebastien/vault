import os

import functionalities.add as funct_add

def delete_account(vault):
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
    os.remove(file)
    vault.content = os.listdir()
    if os.path.exists(file):
        return False
    return True