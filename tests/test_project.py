import pytest

import project
import vault.zip as arch
import vault.vault as vlt

from io import StringIO


def test_get_welcome(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("test\ntest\n"))
    vlt = project.get_welcome()
    assert vlt != None

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


def test_do_function(monkeypatch):
    mock_input = StringIO("15\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    result = project.do_function("generate") 
    assert result.isalnum() == True




