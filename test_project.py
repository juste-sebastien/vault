import sys
import os
import csv

import pytest

import project
import class_vault as vlt

from io import StringIO


def count_lines(vault):
    with open(vault.file, "r") as f:
        count_lines = 0
        fieldnames = ["account", "login", "password", "url"]
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=",")
        for row in reader:
            count_lines += 1
        return count_lines


def test_get_choice(monkeypatch):

    mock_input = StringIO("consult\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert project.get_choice() == "consult"

    mock_input = StringIO("add\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert project.get_choice() == "add"

    mock_input = StringIO("quit\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert project.get_choice() == "quit"

    mock_input = StringIO("generate\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert project.get_choice() == "generate"

    mock_input = StringIO("usage\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert project.get_choice() == "usage"

    mock_input = StringIO("test\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert project.get_choice() == "usage"

def test_consult(monkeypatch):
    vault = vlt.Vault("test", "test")
    project.undo_zip(vault.archive, vault.password)
    
    def mockreturn(mode, vault):
        row = {"account": "add", "login": "add", "password": "add", "url": "No url"}
        return row["account"], row["login"], row["password"], row["url"]

    monkeypatch.setattr(project, "search", mockreturn)
    assert project.consult("r", vault) == "Your login for add is add\nthe password associated is add\n"


def test_add(monkeypatch):
    vault = vlt.Vault("test", "test")
    project.undo_zip(vault.archive, vault.password)
    before = count_lines(vault)
    monkeypatch.setattr("sys.stdin", StringIO("add\nadd\nadd\n\n"))
    project.add(vault.file, "a")
    after = count_lines(vault)
    assert after == before + 1

def test_generate(monkeypatch):
    mock_input = StringIO("15\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert len(project.generate()) == 15

    with pytest.raises(ValueError) as exc_info:
        mock_input = StringIO("test\n")
        monkeypatch.setattr("sys.stdin", mock_input)
        project.generate()
    assert exc_info.type is ValueError
    mock_input = StringIO("15\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    pwd_test = project.generate()
    assert not "," in pwd_test == True
    assert not '"' in pwd_test == True
    assert not "'" in pwd_test == True
    assert not "`" in pwd_test == True

def test_check_existance():
    true_vault = vlt.Vault("test", "test")
    false_vault = vlt.Vault("false", "test")

    assert os.path.exists(true_vault.archive) == True
    assert os.path.exists(false_vault.archive) == False

def test_search(monkeypatch):
    vault = vlt.Vault("test", "test")
    project.undo_zip(vault.archive, vault.password)

    with pytest.raises(KeyboardInterrupt) as exc_info:
        mock_input = StringIO("quit\n")
        monkeypatch.setattr(sys, "stdin", mock_input)
        project.search("r",vault)
    assert exc_info.type is KeyboardInterrupt

    with pytest.raises(EOFError) as exc_info:
        mock_input = StringIO("not valid\n")
        monkeypatch.setattr(sys, "stdin", mock_input)
        project.search("r",vault)
    assert exc_info.type is EOFError
    mock_input = StringIO("test\n")
    monkeypatch.setattr(sys, "stdin", mock_input)
    assert project.search("r", vault) == ("test","test","test","test")

def test_create():
    vault2 = vlt.Vault("pikachu", "test")
    project.create(vault2, mode="w")
    assert os.path.exists(vault2.archive) == True
    os.remove(vault2.archive)

def test_formate_url():
    assert project.formate_url("google.com") == "http://www.google.com"
    assert project.formate_url("www.google.com") == "http://www.google.com"

def test_save():
    vault = vlt.Vault("test", "test")
    project.undo_zip(vault.archive, vault.password)
    assert project.save(vault) == "\n Thank's for using Vault"
    assert not os.path.exists(vault.file) == True
    assert os.path.exists(vault.archive) == True

