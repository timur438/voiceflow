import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from hashlib import sha256

def generate_encrypted_key(password: str):
    key = os.urandom(32) 
    salt = os.urandom(16)
    derived_key = PBKDF2(password, salt, dkLen=32) 
    cipher = AES.new(derived_key, AES.MODE_GCM)
    encrypted_key, tag = cipher.encrypt_and_digest(key)
    return salt + cipher.nonce + encrypted_key + tag

def decrypt_key(password: str, encrypted_data: bytes):
    salt = encrypted_data[:16]
    nonce = encrypted_data[16:32]
    ciphertext = encrypted_data[32:-16]
    tag = encrypted_data[-16:]
    derived_key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(derived_key, AES.MODE_GCM, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)