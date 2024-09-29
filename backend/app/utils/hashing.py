import hashlib
import os

def hash_password(password: str):
    salt = os.urandom(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwdhash.hex(), salt.hex()

def check_password(password: str, hashed_password: str, salt: str):
    salt = bytes.fromhex(salt)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwdhash.hex() == hashed_password
