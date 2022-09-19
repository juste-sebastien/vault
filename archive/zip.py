import os
import zipfile

import pyminizip


def undo_zip(archive, pwd):
    """
    Uncompress the archive with the associated pwd

    Parameters:
    -----------------
    archive: str
        A "archive" str is returned by calling vault.archive
    pwd: getpass object
        "pwd" is a getpass object returned by calling vault.get_password()

    Returns:
    -----------------
        None
    """
    pyminizip.uncompress(archive, pwd, "./", 5)


def do_zip(archive, file, pwd):
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
        None
    """
    pyminizip.compress(file, None, archive, pwd, 5)


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
        with a.open(vault.file, mode) as f:
            return None


def check_existance(archive):
    """
    Check if the file exist in the current folder

    Parameters:
    -----------------
    archive: str
        "archive" str returned by calling vault.archive

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
    if os.path.exists(archive):
        return True
    else:
        return False
