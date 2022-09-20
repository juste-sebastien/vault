import json

from base64 import b64decode

from Crypto.Cipher import ChaCha20_Poly1305

# We assume that the key was securely shared beforehand
def decrypt(vault, row):
    try:

        b64 = json.loads(row)

        jk = [ 'nonce', 'header', 'ciphertext', 'tag' ]

        jv = {k:b64decode(b64[k]) for k in jk}

        cipher = ChaCha20_Poly1305.new(key=key, nonce=jv['nonce'])

        cipher.update(jv['header'])

        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        print(plaintext)

        return plaintext

    except (ValueError, KeyError):

        print("Incorrect decryption")