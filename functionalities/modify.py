import getpass

import vault.vault as vlt
import vault.account as account
import functionalities.add as funct_add

import functionalities.consult as funct_consult

def do_modifying(vault):
    prompt = "Which account do you want modify? "
    try:
        account = funct_consult.search("r", vault, prompt)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except EOFError:
        raise EOFError

    parameter = get_parameter()

    if change_set(account, parameter):
        text = {"account": account.name, "login": account.login, "pwd": account.pwd, "url": account.url}
        row = {"nonce": "", "header": "", "ciphertext": text, "tag": ""}
        account.setting = row
        return funct_add.save_file(account, vault, "w", "modified")
    else:
        return "Sorry, we can't modifying your account"

def get_parameter():
    try:
        parameter = str(input("Which parameter do you want to change? "))
    except:
        print("I'm sorry, but i've don't understand what you want. Please try again.")
        return get_parameter()
    else:
        if parameter in ["name", "n", "login", "l", "password", "p", "pwd", "url", "u"]:
            return parameter
        else:
            print("Options: name or n\n\t\tlogin or l\n\t\tpassword or p\n\t\turl or u")
            return get_parameter()


def change_set(account, parameter):
    if parameter in ["name", "n"]:
        account.name = str(input("New account name: "))
        return True
    elif parameter in ["login", "l"]:
        account.login = str(input("New account login: "))
        return True
    elif parameter in ["password", "pwd", "p"]:
        account.pwd = getpass.getpass()
        return True
    elif parameter in ["url", "u"]:
        account.url = str(input("New account name: "))
        return True
    else:
        return False

    

    
