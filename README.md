# Vault App
***
Copyright 2022 Sébastien Juste


## Table of Contents
1. [Video Demo](#video-demo)
2. [Description](#description)
3. [Compatibilities](#compatibilities)
4. [Installation](#installation)
5. [Functions](#functions)
6. [Features](#features)
7. [Contributing](#contributing)


#### Video Demo: [click here](https://youtu.be/gkvQTWA7YEw)
***


#### Description:
***
This is my project to cloturate the CS50p. The programm interact with the user to create a Vault, crypt it with a password, store all of the set of login password and url tha he want and generate some password


#### Compatibilities
***
Python 3.6+


#### Installation
***
Please read `requirements.txt` to get all libs using with this project and use the package manager [pip](https://pip.pypa.io/en/stable/) to install them.

```bash
git clone https://github.com/juste-sebastien/vault
cd path/to/the/file
python3 project.py
```


##### Functions
***

**get_welcome():**
    Print usage of the app and create a vault object. If the vault not exist,
    a new vault is created by calling `create()`.

    Parameters:
    -----------------
    None

    Returns:
    -----------------
    vault: a Vault object

**get_choice():**
    Prompt user to make a choice for using vault
    User could choose between consult, add, generate, usage and quit 
    if not, function returns usage

    Parameters:
    -----------------
    vault: Vault object from class_vault.py

    Returns:
    -----------------
    choice: str
        The choice in the list: consult, add, generate, usage or quit


**consult():**
    Open personal vault decrypt it if password correspond to the archive where encrypt with
    Print login and password for a specified account register in the vault

    Parameters:
    -----------------
    vault: Vault object
    mode: str
        "mode" to give the parameter of `open()` `r` for reading and `w` for writing

    Returns:
    -----------------
     f-str: str
        A formatted string with account, login, password and if exist url


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
    No return


**generate():**
    Generate a random password from the ASCII table, including lower and uppercase,
    numbers, and all specials characters excluded " ' ` and ,

    Parameters:
    -----------------

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
    row[""]: tuple
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

**formate_url():**
    Formate an url "google.com" to the format "http://wwww.google.com"

    Parameters:
    -----------------
    url: str
        give by user when he add an account
    
    Returns:
    -----------------
    f-string: str
        a formatted string like "http://www.google.com"

**save():**
    Call do_zip() to compress the archive and remove csv file

    Parameters:
    -----------------
    vault: a Vault object

    Returns:
    -----------------
    str
        a comment to close Vault app and granted user


#### Features
***
- [X] Crypted entire file
- [ ] Add a GUI
- [ ] Add a DB to keep vault on a server
- [ ] Create a mozila applet


#### Contributing
***
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.