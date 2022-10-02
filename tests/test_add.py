from io import StringIO

import functionalities.add as funct_add
import vault.vault as vlt

import pytest


def test_not_existing(monkeypatch):
    vault = vlt.Vault("test", "test")
    mock_input = StringIO("no\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    with pytest.raises(KeyboardInterrupt) as exc_info:
        funct_add.not_existing(vault)
    assert exc_info.type == KeyboardInterrupt


def test_add(monkeypatch):
    vault = vlt.Vault("test", "test")
    mock_input = StringIO("test\ntest\ntest\ntest.com\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    account = funct_add.add(vault)
    assert account.name == "test"
    assert account.setting == {
        "nonce": "",
        "header": "",
        "ciphertext": {
            "account": account.name,
            "login": account.login,
            "pwd": account.pwd,
            "url": account.url,
        },
        "tag": "",
    }
