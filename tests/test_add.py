def test_add(monkeypatch):
    vault = vlt.Vault("test", "test")
    arch.undo_zip(vault.archive, vault.password)
    before = count_lines(vault)
    monkeypatch.setattr("sys.stdin", StringIO("add\nadd\nadd\n\n"))
    project.add(vault.file, "a")
    after = count_lines(vault)
    assert after == before + 1
