import sys

import zipfile
import pyminizip

import project
import class_vault as vlt

from io import StringIO


def test_consult(monkeypatch):
    vault = vlt.Vault("cabron", "test")
    pyminizip.uncompress(vault.archive, vault.password, "./", 5)
    with open(vault.file, "r") as f:
        monkeypatch.setattr("sys.stdin", StringIO("test"))
        pathfile = "./" + vault.file
        assert project.consult(vault.file, pathfile, "r") == "Your login for test is test\nthe password associated is test\n"

def test_add(monkeypatch):
    vault = vlt.Vault("cabron", "test")
    pyminizip.uncompress(vault.archive, vault.password, "./", 5)
    with open(vault.file, "r") as f:
        monkeypatch.setattr("sys.stdin", StringIO("test\ntest\ntest\ntest.com"))
        assert project.add(vault.file, "a") == None


def test_generate():
    pwd_generated = project.generate(15)
    assert len(pwd_generated) == 15
    assert pwd_generated.isascii() == True


def test_check_existance():
    vault = vlt.Vault("cabron", b"test")
    pyminizip.uncompress(vault.archive, vault.password, "./", 5)
    with open(vault.file, "r") as f:
        assert project.check_existance(vault.archive, vault.file, "r", vault.password) == True


def test_search(monkeypatch):
    vault = vlt.Vault("cabron", b"test")
    pyminizip.uncompress(vault.archive, vault.password, "./", 5)
    with open(vault.file, "r") as f:
        monkeypatch.setattr("sys.stdin", StringIO("test"))
        assert project.search(vault.file, "r") == ("test","test","test","test.com")


def test_create():
    vault = vlt.Vault("test", b"test")
    assert project.create(vault, "w") == None
