from io import StringIO

import functionalities.modify as modify
import vault.vault as vlt
import vault.account as acnt


def test_change_set(monkeypatch):
    account = acnt.Account("test", "test", "test", "No url")
    mockinput = StringIO("modified\n")
    monkeypatch.setattr("sys.stdin", mockinput)
    assert modify.change_set(account, "n") == True

    mockinput = StringIO("modified\n")
    monkeypatch.setattr("sys.stdin", mockinput)
    assert modify.change_set(account, "name") == True

    mockinput = StringIO("modified\n")
    monkeypatch.setattr("sys.stdin", mockinput)
    assert modify.change_set(account, "password") == True

    mockinput = StringIO("modified\n")
    monkeypatch.setattr("sys.stdin", mockinput)
    assert modify.change_set(account, "url") == True

    mockinput = StringIO("modified\n")
    monkeypatch.setattr("sys.stdin", mockinput)
    assert modify.change_set(account, "l") == True

    mockinput = StringIO("modified\n")
    monkeypatch.setattr("sys.stdin", mockinput)
    assert modify.change_set(account, "p") == True

    mockinput = StringIO("modified\n")
    monkeypatch.setattr("sys.stdin", mockinput)
    assert modify.change_set(account, "u") == True

    monkeypatch.setattr("sys.stdin", mockinput)
    assert modify.change_set(account, "pwd") == True

    monkeypatch.setattr("sys.stdin", mockinput)
    assert modify.change_set(account, "test") == False
