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
