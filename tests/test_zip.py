import os

import classes.vault as vlt
import archive.zip as zip


def test_create():
    vault2 = vlt.Vault("pikachu", "test")
    zip.create(vault2, mode="w")
    assert os.path.exists(vault2.archive) == True
    os.remove(vault2.archive)

def test_check_existance():
    true_vault = vlt.Vault("test", "test")
    false_vault = vlt.Vault("false", "test")

    assert os.path.exists(true_vault.archive) == True
    assert os.path.exists(false_vault.archive) == False
