# Python.CryptographyKeyManagement.json -> "Cryptography Key Management Python" [KeyManagementService]
# Expected: method cryptography MultiFernet (key rotation)
from cryptography.fernet import Fernet, MultiFernet


def build_keyring(current_key: bytes, previous_keys: list[bytes]) -> MultiFernet:
    return MultiFernet([Fernet(current_key)] + [Fernet(key) for key in previous_keys])


def rotate(keyring: MultiFernet, ciphertexts: list[bytes]) -> list[bytes]:
    return [keyring.rotate(token) for token in ciphertexts]


def encrypt(keyring: MultiFernet, plaintext: bytes) -> bytes:
    return keyring.encrypt(plaintext)


def decrypt(keyring: MultiFernet, token: bytes) -> bytes:
    return keyring.decrypt(token)
