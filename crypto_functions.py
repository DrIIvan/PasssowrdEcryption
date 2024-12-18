from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


def AES256_encryption(data: bytes, key: bytes):
    cipher = Cipher(algorithms.AES256(key), modes.CBC(b'8tX\xcbtxj\xf8\xa7n\xe9w%\x12\x86\x01'))
    encryptor = cipher.encryptor()
    encrypted_text = encryptor.update(data) + encryptor.finalize()
    return encrypted_text


def AES256_decryption(data: bytes, key: bytes):
    cipher = Cipher(algorithms.AES256(key), modes.CBC(b'8tX\xcbtxj\xf8\xa7n\xe9w%\x12\x86\x01'))
    decryptor = cipher.decryptor()
    return str(decryptor.update(data) + decryptor.finalize())[2:-1]


def add_bytes(data: str, key_size_in_bytes: int):
    if len(data) % key_size_in_bytes != 0:
        data += "^"
        while len(data) % key_size_in_bytes != 0:
            data += "0"
        return data
    else:
        return data


def clear_added_bytes(data: str):
    return data[:data.find("^")]


def get_random_key(size: int):
    return os.urandom(size)
