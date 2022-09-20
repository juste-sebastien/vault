import json

from vault import vault as vlt

from base64 import b64encode

from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes

def encrypt(vault, plaintext):
    key = vault.password

    while len(key) < 32:
        for i in range(len(vault.password)):
            if len(key) > 32:
                break
            key += vault.password[i]

    header = bytes(vault.login.encode("utf-8"))
    plaintext = bytes(plaintext.encode("utf-8"))

    key = bytes(key.encode("utf-8"))

    cipher = ChaCha20_Poly1305.new(key=key)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    jk = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    jv = [ b64encode(x).decode('utf-8') for x in (cipher.nonce, header, ciphertext, tag) ]

    result = json.dumps(dict(zip(jk, jv)))

    print(result)
    return result