# CS50's Vault Project
Copyright 2022 Sébastien Juste

#### Video Demo: [click here](todo)


#### Description:
This is my project to cloturate the CS50p. The programm interact with the user to create a Vault, crypt it with a password, store all of the set of login password and url tha he want and generate some password


#### Compatibilities
Python 3.6+


#### Installation
Please read `requirements.txt` to get all libs using with this project and use the package manager [pip](https://pip.pypa.io/en/stable/) to install them.

```bash
pip install [module_name]
```


##### Function

**get_welcome():**
    Print usage of the app and create a vault object. If the vault not exist,
    a new vault is created by calling `create()`. Finally, `get_choice()` is called

    Parameters:
    -----------------
        None

    Returns:
    -----------------
        Call `get_choice()`

**get_choice():**
    Extract csv from zip archive corresponding to vault
    Prompt user to make a choice for using vault
    User could choose between consult, add, generate, usage and quit

    Parameters:
    -----------------
        vault: Vault object from class_vault.py

    Returns:
    -----------------
        None


**consult():**
    Open personal vault decrypt it if password correspond to the archive where encrypt with
    Print login and password for a specified account register in the vault

    Parameters:
    -----------------
    file: str
        A "file" str is returned by calling vault.file
    pathfile: str
        "pathfile" is the name of the "file" transformed to path `./[filename]`
    mode: str
        "mode" to give the parameter of `open()` `r` for reading and `w` for writing

    Returns:
    -----------------
        None



**add():**
    Add a new account on the csv file representing the vault

    Parameters:
    -----------------
        file: str
            A "file" str is returned by calling `vault.file`
        mode: str
            "mode" to give the parameter of `open()` `a` for append to the current vault

    Returns:
    -----------------
        None


**generate():**
    Generate a random password from the ASCII table, including lower and uppercase,
    numbers, and all specials characters

    Parameters:
    -----------------
        length: int
            "length" is given by user with a prompt

    Returns:
    -----------------
        pwd_created: str
            "pwd_created" is a random password created for the user



**check_existance():**
    Check if the file exist in the current folder
    
    Parameters:
    -----------------
    file: str
        A "file" str is returned by calling `vault.file`
    archive: str
        "archive" str returned by calling `vault.archive`
    mode: str
        "mode" to give the parameter of `open()` `r` for reading and `w` for writing
    pwd: getpass object
        "pwd" is a getpass object returned by calling `vault.get_password()`

    Returns:
    -----------------
        True
            if the file exist
        False
            if not

    Exceptions:
    -----------------
        FileNotFoundError
        IOError


**search():**
    Search the account, login, pwd and url in the csv file

    Parameters:
    -----------------
    file: str
        A "file" str is returned by calling `vault.file`
    mode: str
        "mode" to give the parameter of `open()` `r` for reading and `w` for writing

    Returns:
    -----------------
        row[""]
            only if a corresponding row was found


**create():**
    Create a new vault with an archive and a csv file 

    Parameters:
    -----------------
    vault: vault object
    mode: str
        "mode" to give the parameter of `open()` `r` for reading and `w` for writing

    Returns:
    -----------------
        None


**undo_zip():**
    Uncompress the archive with the associated pwd

    Parameters:
    -----------------
    archive: str
        A "archive" str is returned by calling `vault.archive`
    pwd: getpass object
        "pwd" is a getpass object returned by calling `vault.get_password()`

    Returns:
    -----------------
        None



**do_zip():**
    Compress the archive with the associated pwd

    Parameters:
    -----------------
    archive: str
        A "archive" str is returned by calling `vault.archive`
    pwd: getpass object
        "pwd" is a getpass object returned by calling `vault.get_password()`

    Returns:
    -----------------
        None


#### Features

- [ ] Crypted entire file with rsa or sha512
- [ ] Add a GUI

#### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.