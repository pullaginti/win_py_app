# encryption_utils.py
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import os

def encrypt_file(file_path, password):
    key = PBKDF2(password, b'salt', dkLen=32)
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    with open(file_path + '.enc', 'wb') as f:
        f.write(nonce)
        f.write(tag)
        f.write(ciphertext)

    os.remove(file_path)

def decrypt_file(file_path, password):
    key = PBKDF2(password, b'salt', dkLen=32)

    with open(file_path, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        return None

    original_file_path = file_path.replace('.enc', '')
    with open(original_file_path, 'wb') as f:
        f.write(plaintext)

    return original_file_path
