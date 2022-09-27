def test_search(monkeypatch):
    vault = vlt.Vault("test", "test")
    arch.undo_zip(vault.archive, vault.password)

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

def test_consult(monkeypatch):
    vault = vlt.Vault("test", "test")
    arch.undo_zip(vault.archive, vault.password)
    
    def mockreturn(mode, vault):
        row = {"account": "add", "login": "add", "password": "add", "url": "No url"}
        return row["account"], row["login"], row["password"], row["url"]

    monkeypatch.setattr(project, "search", mockreturn)
    assert project.consult("r", vault) == "Your login for add is add\nthe password associated is add\n"
