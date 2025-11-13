# primitives.py
# Cryptographic primitives: hashing, signing, encryption

import hashlib
import hmac
from cryptography.fernet import Fernet

def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def sign_data(data: str, key: str) -> str:
    return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()

def generate_key() -> str:
    return Fernet.generate_key().decode()

def encrypt_data(data: str, key: str) -> str:
    f = Fernet(key.encode())
    return f.encrypt(data.encode()).decode()

def decrypt_data(token: str, key: str) -> str:
    f = Fernet(key.encode())
    return f.decrypt(token.encode()).decode()
