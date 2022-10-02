import crypt.encrypt


def test_generate_key():
    key = "testtesttesttesttesttesttesttest"
    assert crypt.encrypt.generate_key("test") == bytes(key.encode("utf-8"))
