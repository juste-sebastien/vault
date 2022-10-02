import pytest

import main
import functionalities.consult as consult
import vault.vault as vlt
import vault.account as account

from io import StringIO


def test_search(monkeypatch):
    vault = vlt.Vault("test", "test")

    with pytest.raises(KeyboardInterrupt) as exc_info:
        mock_input = StringIO("quit\n")
        monkeypatch.setattr("sys.stdin", mock_input)
        consult.search("r", vault, "")
    assert exc_info.type is KeyboardInterrupt

    with pytest.raises(EOFError) as exc_info:
        mock_input = StringIO("not valid\n")
        monkeypatch.setattr("sys.stdin", mock_input)
        consult.search("r", vault, "")
    assert exc_info.type is EOFError


def test_consult(monkeypatch):
    vault = vlt.Vault("test", "test")

    def mockreturn(mode, vault, prompt):
        acnt = account.Account("add", "add", "add", "No url")
        return acnt

    monkeypatch.setattr("functionalities.consult.search", mockreturn)
    assert (
        consult.consult("r", vault)
        == "Your login for add is add\nthe password associated is add\n"
    )


def test_formate_url():
    assert consult.formate_url("test.com") == "http://www.test.com"
    assert consult.formate_url("http://test.com") == "http://www.test.com"
    assert consult.formate_url("https://test.com") == "https://www.test.com"
