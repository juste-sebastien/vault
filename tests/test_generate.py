from io import StringIO
import pytest

import string

import functionalities.generate as generate


def test_generate():
    assert len(generate.generate(15)) == 15

    alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    digit = list(string.digits)
    spec = list(string.punctuation)
    char_list = alphabet + digit + spec
    pwd_test = generate.generate(15, char_list)
    assert not "," in pwd_test == True
    assert not '"' in pwd_test == True
    assert not "'" in pwd_test == True
    assert not "`" in pwd_test == True


def test_choose_pwd_length(monkeypatch):
    mock_input = StringIO("15\n")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert len(generate.choose_pwd_length()) == 15


def test_choose_special_chars(monkeypatch):
    alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    digit = list(string.digits)
    spec = ["!","\#", "$", "%", "&", "*", "+", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "\\", "."]
    char_list = alphabet + digit + spec
    mock_input = StringIO("ads")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert generate.choose_special_chars == char_list

    digit = list(string.digits)
    spec = ["!","\#", "$", "%", "&", "*", "+", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "\\", "."]
    char_list = digit + spec
    mock_input = StringIO("ds")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert generate.choose_special_chars == char_list

    spec = ["!","\#", "$", "%", "&", "*", "+", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "\\", "."]
    char_list = spec
    mock_input = StringIO("s")
    monkeypatch.setattr("sys.stdin", mock_input)
    assert generate.choose_special_chars == char_list


