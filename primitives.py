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

#
#
#

age = 30           # int
temp = 98.6        # float
active = False     # bool
greeting = "Hi!"   # str

int("42")       # 42
float("3.14")   # 3.14
str(100)        # "100"
bool(0)         # False

if "":         # False
    print("Won't run")
if "hello":    # True
    print("Will run")




