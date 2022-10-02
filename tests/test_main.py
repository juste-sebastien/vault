import pytest

import main
import vault.zip as arch
import vault.vault as vlt

from io import StringIO


def test_get_welcome(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("test\ntest\n"))
    vlt = main.get_welcome()
    assert vlt != None


def test_get_choice(monkeypatch):

    mock_input = StringIO("consult\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert main.get_choice() == "consult"

    mock_input = StringIO("add\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert main.get_choice() == "add"

    mock_input = StringIO("generate\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert main.get_choice() == "generate"

    mock_input = StringIO("usage\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert main.get_choice() == "usage"

    mock_input = StringIO("test\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert main.get_choice() == "usage"

    mock_input = StringIO("list\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert main.get_choice() == "list"

    mock_input = StringIO("modify\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert main.get_choice() == "modify"

    mock_input = StringIO("delete\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert main.get_choice() == "delete"

    with pytest.raises(KeyboardInterrupt) as exc_info:
        mock_input = StringIO("quit\n")
        monkeypatch.setattr("sys.stdin", mock_input)
        main.get_choice()
    assert exc_info.type == KeyboardInterrupt


def test_do_function(monkeypatch):
    vault = vlt.Vault("test", "test")
    mock_input = StringIO("15\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    result = main.do_function("generate", vault)
    assert len(result) == 15

    result = main.do_function("usage", vault)
    assert result == main.USAGE
