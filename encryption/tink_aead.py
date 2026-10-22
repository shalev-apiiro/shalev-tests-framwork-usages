# Python.Tink.json -> "Google Tink Python" [Encryption], vendor Google
# Expected: import tink (tink.aead)
import os

import tink
from tink import aead, secret_key_access

aead.register()


def load_field_cipher(keyset_json: str) -> aead.Aead:
    keyset_handle = tink.json_proto_keyset_format.parse(keyset_json, secret_key_access.TOKEN)
    return keyset_handle.primitive(aead.Aead)


field_cipher = None


def get_cipher() -> aead.Aead:
    global field_cipher
    if field_cipher is None:
        field_cipher = load_field_cipher(os.environ["FIELD_KEYSET_JSON"])
    return field_cipher


def encrypt_field(record_id: str, plaintext: str) -> bytes:
    # Binding the record id as associated data stops a ciphertext being copied onto another record.
    return get_cipher().encrypt(plaintext.encode("utf-8"), record_id.encode("utf-8"))


def decrypt_field(record_id: str, ciphertext: bytes) -> str:
    return get_cipher().decrypt(ciphertext, record_id.encode("utf-8")).decode("utf-8")
