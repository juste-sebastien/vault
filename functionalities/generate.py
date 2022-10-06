import random
import string


SPEC_CHARS = ["!","\#", "$", "%", "&", "*", "+", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "\\", "."]
ALPHABET = list(string.ascii_lowercase) + list(string.ascii_uppercase)
DIGIT = list(string.digits)

def generate(char_numb=0, char_list=[]):
    """
    Generate a random password from the ASCII table, including lower and uppercase,
    numbers, and all specials characters excluded " ' ` and ,

    Parameters:
    -----------------


    Returns:
    -----------------
    pwd_created: str
        "pwd_created" is a random password created for the user
    """
    if char_numb == 0 and char_list == []:
        char_numb = choose_pwd_length()
        char_list = choose_special_chars()
    pwd_created = ""
    i = 0
    while i < char_numb:
        char = random.randint(32, 127)
        if not chr(char) in char_list:
            pass
        else:
            pwd_created += chr(char)
            i += 1
    return pwd_created


def choose_pwd_length():
    try:
        pwd_length = int(input("Which length do you want for your Password? "))
    except (ValueError, TypeError):
        print("You need to type an integer")
        choose_pwd_length()
    else:
        return pwd_length


def choose_special_chars():
    prompt = "What type of characters do you want?\n"+"a for alphabet\n"+"d for digits\n"+"s for specials characters\n"
    char_list = []
    try:
        chars_wanted = str(input(prompt))
    except:
        print("Accepting only a, d and s")
        choose_special_chars()
    else:
        if "a" in chars_wanted:
            char_list += ALPHABET
        if "d" in chars_wanted:
            char_list += DIGIT
        if "s" in chars_wanted:
            char_list += SPEC_CHARS
    return char_list


