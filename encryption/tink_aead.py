# Python.Tink.json -> "Google Tink Python" [Encryption], vendor Google
# Expected: import tink (tink.aead)
import tink
from tink import aead

aead.register()


def new_primitive() -> aead.Aead:
    keyset_handle = tink.new_keyset_handle(aead.aead_key_templates.AES256_GCM)
    return keyset_handle.primitive(aead.Aead)


def encrypt(primitive: aead.Aead, plaintext: bytes, associated_data: bytes) -> bytes:
    return primitive.encrypt(plaintext, associated_data)


def decrypt(primitive: aead.Aead, ciphertext: bytes, associated_data: bytes) -> bytes:
    return primitive.decrypt(ciphertext, associated_data)
