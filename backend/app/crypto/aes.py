from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


def encrypt_data(data, key):

    nonce = os.urandom(12)
    aes = AESGCM(key)

    cipher = aes.encrypt(nonce, data, None)

    return nonce, cipher


def decrypt_data(nonce, cipher, key):

    aes = AESGCM(key)

    return aes.decrypt(nonce, cipher, None)
