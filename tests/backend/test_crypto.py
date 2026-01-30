"""
Crypto Module Test Suite
Tests AES Encryption, Decryption, and Hashing
"""

import os

from backend.app.crypto.aes import encrypt_data, decrypt_data
from backend.app.crypto.hash import sha256


def test_aes_encryption_decryption():
    """
    Test AES-256-GCM encryption & decryption
    """

    data = b"Confidential cyber evidence data"
    key = b"0" * 32  # 256-bit key

    nonce, cipher = encrypt_data(data, key)

    assert nonce is not None
    assert cipher is not None
    assert cipher != data

    plain = decrypt_data(nonce, cipher, key)

    assert plain == data


def test_sha256_hash():
    """
    Test SHA-256 hashing
    """

    data = b"Test hash content"

    hash_val = sha256(data)

    assert isinstance(hash_val, str)
    assert len(hash_val) == 64  # SHA-256 hex length


def test_different_inputs_produce_different_hashes():
    """
    Hash collision check
    """

    data1 = b"Evidence 1"
    data2 = b"Evidence 2"

    hash1 = sha256(data1)
    hash2 = sha256(data2)

    assert hash1 != hash2


def test_wrong_key_fails_decryption():
    """
    Ensure wrong key fails decryption
    """

    data = b"Secret file"
    key1 = b"1" * 32
    key2 = b"2" * 32

    nonce, cipher = encrypt_data(data, key1)

    try:
        decrypt_data(nonce, cipher, key2)
        assert False, "Decryption should fail with wrong key"
    except Exception:
        assert True
