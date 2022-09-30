from io import StringIO
import pytest

import functionalities.generate as generate


def test_generate(monkeypatch):
    mock_input = StringIO("15\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert len(generate.generate()) == 15

    mock_input = StringIO("15\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    pwd_test = generate.generate()
    assert not "," in pwd_test == True
    assert not '"' in pwd_test == True
    assert not "'" in pwd_test == True
    assert not "`" in pwd_test == True
