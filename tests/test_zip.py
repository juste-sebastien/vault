import os

from vault import vault
from vault import zip

def test_create():
    vault2 = vault.Vault("pikachu", "test")
    zip.create(vault2, mode="w")
    assert os.path.exists(vault2.archive) == True
    os.remove(vault2.archive)

def test_check_existance():
    true_vault = vault.Vault("test", "test")
    false_vault = vault.Vault("false", "test")

    assert os.path.exists(true_vault.archive) == True
    assert os.path.exists(false_vault.archive) == False

def test_save():
    vlt = vault.Vault("test", "test")
    zip.undo_zip(vlt.archive, vlt.password)
    assert zip.save(vlt) == "\n Thank's for using Vault"
    assert not os.path.exists(vlt.file) == True
    assert os.path.exists(vlt.archive) == True


