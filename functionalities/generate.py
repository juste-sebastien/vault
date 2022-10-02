import random


def generate():
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
    try:
        pwd_length = int(input("Which length do you want for your Password? "))
    except (ValueError, TypeError):
        print("You need to type an integer")
        generate()
    else:
        pwd_created = ""
        i = 0
        while i < pwd_length:
            char = random.randint(32, 127)
            if chr(char) in ['"', "'", "`", ","]:
                pass
            else:
                pwd_created += chr(char)
                i += 1
        return pwd_created
