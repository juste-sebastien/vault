import os
import csv

import vault.vault as vlt
import vault.zip as arch

import functionalities.generate as funct_generate
import functionalities.consult as funct_consult
import functionalities.add as funct_add

USAGE = str(
    "\n"
    + "consult -> for consulting a password in your vault\n"
    + "generate -> for generating a new password\n"
    + "add -> for adding a new account(login + password) in to your vault\n"
    + "CTRL + D or CTRL + C or quit -> to save your vault and quit program\n"
    + "usage -> when you don't know what to do"
)


def main():
    try:
        vault = get_welcome()
    except TypeError:
        pass
    else:
        file = vault.file
        archive = vault.archive
        password = vault.password
        path_file = "./" + file
        arch.undo_zip(archive, password)
        while True:
            try:
                choice = get_choice()
                if "quit" in choice:
                    raise KeyboardInterrupt
                elif not choice.isalpha():
                    raise TypeError
            except KeyboardInterrupt:
                break
            except TypeError:
                print(f"{USAGE}")
                pass
            except EOFError:
                break
            else:
                match choice:
                    case "consult":
                        print(f"\nGroovy we're gonna to consult your vault")
                        mode = "r"
                        try:
                            account = funct_consult.consult(mode, vault)
                        except KeyboardInterrupt:
                            break
                        except EOFError:
                            print("Account seems not to be save in your Vault.")
                            want_add = input("Do you want to add it in your Vault? (yes or no) ")
                            if "yes" in want_add:
                                funct_add.add(vault, vault.file, "a+")
                            else:
                                pass
                        except TypeError:
                            pass
                        else:
                            print(account)


                    case "add":
                        print("\nLet's go for adding a new set in to your vault")
                        mode = "a"
                        funct_add.add(vault, file, mode)

                    case "generate":
                        print("\nAmazing, let me create a new PWD for you")
                        try:
                            pwd = funct_generate.generate()
                        except ValueError:
                            funct_generate.generate()
                        except TypeError:
                            funct_generate.generate()
                        else:
                            print(pwd)

                    case "usage":
                        print(f"{USAGE}")
                    case _:
                        pass
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
    print("Welcome in Vault App.\n" + f"{USAGE}\n")
    vault = vlt.Vault.get()
    if not arch.check_existance(vault.archive):
        answer_create = input(
            f"\n {vault.login} does not exist. Do you want to create it? (yes or no) "
        ).lower().strip()
        if answer_create == "yes":
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
    if not choice in ["consult", "add", "generate", "usage", "quit"]:
        return "usage"
    return choice


if __name__ == "__main__":
    main()
