import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from hashlib import sha256
import base64

def generate_encrypted_key(password: str):
    key = base64.b64encode(os.urandom(32)).decode() 
    salt = os.urandom(16)
    derived_key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(derived_key, AES.MODE_GCM)
    encrypted_key, tag = cipher.encrypt_and_digest(key.encode()) 
    return base64.b64encode(salt + cipher.nonce + encrypted_key + tag).decode()

def decrypt_key(password: str, encrypted_data: str):
    encrypted_data_bytes = base64.b64decode(encrypted_data) 
    salt = encrypted_data_bytes[:16]
    nonce = encrypted_data_bytes[16:32]
    ciphertext = encrypted_data_bytes[32:-16]
    tag = encrypted_data_bytes[-16:]
    derived_key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(derived_key, AES.MODE_GCM, nonce)
    decrypted_key = cipher.decrypt_and_verify(ciphertext, tag).decode()
    return decrypted_key