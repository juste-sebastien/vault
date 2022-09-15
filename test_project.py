import sys
import os
import csv

import pytest

import project
import class_vault as vlt

from io import StringIO

"""
def test_get_welcome():
    #verifier la creation d'un objet
    vault = vlt.Vault("test", "test")
    assert vault.login == "test"
    assert vault.password == "test"
    #verifier l'existance d'une archive
    if os.path.exists(vault.archive):
        assert os.path.exists(vault.archive)
"""
def count_lines(vault):
    with open(vault.file, "r") as f:
        count_lines = 0
        fieldnames = ["account", "login", "password", "url"]
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=",")
        for row in reader:
            count_lines += 1
        return count_lines


def test_get_choice(monkeypatch):
    #verifier que l'input consult fonctionne
    mock_input = StringIO("consult\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert project.get_choice() == "consult"
    #verifier que l'input add fonctionne
    mock_input = StringIO("add\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert project.get_choice() == "add"
    #verifier que l'input quit fonctionne
    mock_input = StringIO("quit\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert project.get_choice() == "quit"
    #verifier que l'input generate fonctionne
    mock_input = StringIO("generate\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert project.get_choice() == "generate"
    #verifier que l'input usage fonctionne
    mock_input = StringIO("usage\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert project.get_choice() == "usage"
    #verifier qu'un input quelconque renvoie usage
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
    # verifier que si url n'est pas rentré, No url registered soit inséré
    monkeypatch.setattr("sys.stdin", StringIO("add\nadd\nadd\n\n"))
    project.add(vault.file, "a")
    after = count_lines(vault)
    assert after == before + 1

def test_generate(monkeypatch):
    # verifier que la longueur du mdp soit bien la meme qu'enregistré
    mock_input = StringIO("15\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert len(project.generate()) == 15
    #assert project.generate().isascii() == True
    # verifier qu'un entier soit inseré
    with pytest.raises(ValueError) as exc_info:
        mock_input = StringIO("test\n")
        monkeypatch.setattr("sys.stdin", mock_input)
        project.generate()
    assert exc_info.type is ValueError
    # verifier qu'aucun des caracteres ' " , ` n'apparaissent dans le mdp
    mock_input = StringIO("15\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    pwd_test = project.generate()
    assert not "," in pwd_test == True
    assert not '"' in pwd_test == True
    assert not "'" in pwd_test == True
    assert not "`" in pwd_test == True

#check_existance()
    true_vault = vlt.Vault("test", "test")
    false_vault = vlt.Vault("false", "test")
    #verifier True si un fichier exist
    assert os.path.exists(true_vault.archive) == True
    # False s'il n'existe pas
    assert os.path.exists(false_vault.archive) == False

def test_search(monkeypatch):
    vault = vlt.Vault("test", "test")
    project.undo_zip(vault.archive, vault.password)
    #verifier quit renvoie KeyBoardInterrupt 
    with pytest.raises(KeyboardInterrupt) as exc_info:
        mock_input = StringIO("quit\n")
        monkeypatch.setattr(sys, "stdin", mock_input)
        project.search("r",vault)
    assert exc_info.type is KeyboardInterrupt
    #verifier que si la recherche n'existe pas renvoie EOFError
    with pytest.raises(EOFError) as exc_info:
        mock_input = StringIO("not valid\n")
        monkeypatch.setattr(sys, "stdin", mock_input)
        project.search("r",vault)
    assert exc_info.type is EOFError
    #verifier que si la recherche existe renvoie les éléments de la recherche
    mock_input = StringIO("test\n")
    monkeypatch.setattr(sys, "stdin", mock_input)
    assert project.search("r", vault) == ("test","test","test","test")

def test_create():
    #verifier l'existance d'une archive
    vault2 = vlt.Vault("pikachu", "test")
    project.create(vault2, mode="w")
    assert os.path.exists(vault2.archive) == True
    os.remove(vault2.archive)

def test_formate_url():
    #verifier que nomdedomaine.com soit reformaté en http://www.nomdedomaine.com
    assert project.formate_url("google.com") == "http://www.google.com"
    assert project.formate_url("www.google.com") == "http://www.google.com"

def test_save():
    vault = vlt.Vault("test", "test")
    project.undo_zip(vault.archive, vault.password)
    #verifier de le retour soit bien le message d cloture
    assert project.save(vault) == "\n Thank's for using Vault"
    #verifier que le fichier csv n'existe plus
    assert not os.path.exists(vault.file) == True
    #verfier que le fichier zip existe
    assert os.path.exists(vault.archive) == True

