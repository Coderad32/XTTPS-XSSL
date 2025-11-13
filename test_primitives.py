# test_primitives.py
# Unit tests for crypto primitives

from crypto import primitives

def test_hash():
    assert primitives.hash_data("test") == primitives.hash_data("test")

def test_sign():
    key = "secret"
    assert primitives.sign_data("data", key) == primitives.sign_data("data", key)

def test_encrypt_decrypt():
    key = primitives.generate_key()
    encrypted = primitives.encrypt_data("hello", key)
    decrypted = primitives.decrypt_data(encrypted, key)
    assert decrypted == "hello"
