import pytest

from io import StringIO

import functionalities.delete as delete
import vault.vault as vlt


def test_delete(monkeypatch):
    mockinput = StringIO("quit\n")
    vault = vlt.Vault("test", "test")
    vault.content = ["test.csv"]

    def mockreturn_remove_file(file, vault):
        return True

    with pytest.raises(KeyboardInterrupt) as exc_info:
        monkeypatch.setattr("sys.stdin", mockinput)
        delete.delete_account(vault)
    assert exc_info.type is KeyboardInterrupt

    mockinput = StringIO("test\n")
    monkeypatch.setattr("sys.stdin", mockinput)
    monkeypatch.setattr("functionalities.delete.remove_file", mockreturn_remove_file)
    assert delete.delete_account(vault) == "test was deleted from your Vault"
