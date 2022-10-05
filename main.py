import sys
import os

from curses.ascii import isalnum

import vault.vault as vlt
import vault.zip as arch

import functionalities.generate as funct_generate
import functionalities.consult as funct_consult
import functionalities.add as funct_add
import functionalities.modify as funct_modify
import functionalities.delete as funct_delete

import gui.interface


USAGE = str(
    "\n"
    + "consult -> for consulting a password in your Vault\n"
    + "generate -> for generating a new password\n"
    + "add -> for adding a new account(login + password) in to your Vault\n"
    + "modify -> for modifying an existing account\n"
    + "list -> to see which accounts are saved in to your Vault\n"
    + "CTRL + D or CTRL + C or quit -> to save your vault and quit program\n"
    + "usage -> when you don't know what to do"
)

WARNS = str(
    "\n"
    + "1. Please be sure to be in the same directory of your Vault zip file\n"
    + "\n"
    + "2. You can type any password that you want to get an account set"
    + "but if you can't read it clearly, it's because it's the wrong password.\n"
    + "Vault App don't permitted to recover password.\n"
    + "Keep it in safe place ;)"
)


def main():
    if len(sys.argv) >=2 and sys.argv[1] in ["i", "interface"]:
        gui.interface.run()
    else:
        try:
            vault = get_welcome()
        except TypeError:
            sys.exit("Thank's for using Vault App")

        arch.undo_zip(vault)
        vault.content = os.listdir()

        while True:
            try:
                choice = get_choice()
                result = do_function(choice, vault)
            except KeyboardInterrupt:
                break
            except (EOFError, TypeError):
                break
            else:
                if result.isalnum:
                    print(result)
        print(arch.save(vault))


def get_welcome():
    """
    Print usage of the app and create a vault object. If the vault not exist,
    a new vault is created by calling create().

    Parameters:
    -----------------
    None

    Returns:
    -----------------
    vault:
        a vault object
    """
    print("Welcome in Vault App.\n" + f"{WARNS}\n{USAGE}\n")
    vault = vlt.Vault.get()
    if not arch.check_existance(vault.archive):
        answer_create = (
            input(
                f"\n {vault.login} does not exist. Do you want to create it? (yes or no) "
            )
            .lower()
            .strip()
        )
        if answer_create == "yes" or answer_create == "y":
            arch.create(vault, "w")
        else:
            raise TypeError
    return vault


def get_choice():
    """

    Prompt user to make a choice for using vault
    User could choose between consult, add, generate, usage and quit
    if not, generate returns usage

    Parameters:
    -----------------
    vault: Vault object from class_vault.py

    Returns:
    -----------------
    choice
    """
    choice = input("\nWhat do you want to do? ").lower().strip()
    if "quit" in choice:
        raise KeyboardInterrupt
    if not choice in [
        "consult",
        "add",
        "generate",
        "usage",
        "modify",
        "list",
        "delete",
    ]:
        return "usage"
    return choice


def do_function(choice, vault):
    match choice:
        case "consult":
            print(f"\nGroovy we're gonna to consult your vault")
            mode = "r"
            try:
                account = funct_consult.consult(mode, vault)
            except KeyboardInterrupt:
                return arch.save(vault)
            except EOFError:
                account = funct_add.not_existing(vault)
            except TypeError:
                raise TypeError

            return account

        case "add":
            print("\nLet's go for adding a new set in to your vault")
            mode = "w"
            return funct_add.add(vault)

        case "generate":
            print("\nAmazing, let me create a new PWD for you")
            return funct_generate.generate()

        case "usage":
            return f"{USAGE}"

        case "modify":
            print("\nLet's go to modify an account")
            return funct_modify.do_modifying(vault)

        case "delete":
            print("Oh my god let's deleting an account")
            return funct_delete.delete_account(vault)

        case "list":
            for file in vault.content:
                print(file.strip(".csv"))

        case _:
            raise EOFError


if __name__ == "__main__":
    main()
