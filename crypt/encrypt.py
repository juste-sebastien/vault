import json

from vault import vault as vlt

from base64 import b64encode

from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes


def encrypt(vault, plaintext):
    key = generate_key(vault.password)

    header = bytes(vault.login.encode("utf-8"))
    plaintext = bytes(str(plaintext).encode("utf-8"))

    cipher = ChaCha20_Poly1305.new(key=key)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    jk = ["nonce", "header", "ciphertext", "tag"]
    jv = [b64encode(x).decode("utf-8") for x in (cipher.nonce, header, ciphertext, tag)]

    result = json.dumps(dict(zip(jk, jv)))
    return result


def generate_key(password):
    key = password

    while len(key) < 32:
        for i in range(len(password)):
            if len(key) >= 32:
                break
            key += password[i]
    return bytes(key.encode("utf-8"))
