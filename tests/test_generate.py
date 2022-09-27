
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
