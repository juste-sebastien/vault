import json

from base64 import b64decode

from Crypto.Cipher import ChaCha20_Poly1305

from crypt.encrypt import generate_key

def decrypt(vault, ciphertext):
    try:
        b64 = json.loads(ciphertext)
        jk = [ 'nonce', 'header', 'ciphertext', 'tag' ]
        jv = {k:b64decode(b64[k]) for k in jk}
        key = generate_key(vault.password)

        cipher = ChaCha20_Poly1305.new(key=key, nonce=jv['nonce'])

        cipher.update(jv['header'])

        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])

        return plaintext.decode("utf-8")

    except (ValueError, KeyError):

        print("Incorrect decryption")