import os
import shutil
import zipfile

import pyminizip


def undo_zip(vault):
    """
    Uncompress the archive with the associated pwd in a temporary directory

    Parameters:
    -----------------
    archive: str
        A "archive" str is returned by calling vault.archive
    pwd: getpass object
        "pwd" is a getpass object returned by calling vault.get_password()

    Returns:
    -----------------
    f-string: str
        name of temporary directory

    """
    vault.temp = f"{vault.parent}/{vault.login}/"
    try:
        os.mkdir(vault.temp)
    except FileExistsError:
        pass
    
    os.chdir(vault.temp)
    try:
        pyminizip.uncompress(vault.path, vault.password, vault.temp, 1)
    except OSError:
        pass


def do_zip(vault):
    """
    Compress the archive with the associated pwd

    Parameters:
    -----------------
    archive: str
        A "archive" str is returned by calling vault.archive
    pwd: getpass object
        "pwd" is a getpass object returned by calling vault.get_password()

    Returns:
    -----------------
        No return
    """
    file_list = os.listdir(vault.temp)
    path_list =[]
    for _ in range(len(file_list)):
        file_path = vault.temp
        path_list.append(file_path)
    if len(file_list) != 1:
        pyminizip.compress_multiple(file_list, [], vault.archive, vault.password, 5)
    else:
        pyminizip.compress(file_list[0], None, vault.archive, vault.password, 5)
    
    if check_existance(vault.path):
        os.remove(vault.path)
    
    shutil.move(vault.archive, "../")

    



def create(vault, mode):
    """
    Create a new vault with an archive and a csv file

    Parameters:
    -----------------
    vault: vault object
    mode: str
        "mode" to give the parameter of open() r for reading and w for writing

    Returns:
    -----------------
    None
    """
    with zipfile.ZipFile(vault.archive, mode) as a:
        return None


def check_existance(file):
    """
    Check if the file exist in the current folder

    Parameters:
    -----------------
    file: str
        the path of the file which need to check existance

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
    """
    if os.path.exists(file):
        return True
    else:
        return False


def save(vault):
    """
    Call do_zip() to compress the archive and remove csv fil

    Parameters:
    -----------------
    vault: a Vault object

    Returns:
    -----------------
    str
        a comment to close Vault app and granted user
    """
    do_zip(vault)
    os.chdir("../")
    shutil.rmtree(vault.temp)
    return "\n Thank's for using Vault"
