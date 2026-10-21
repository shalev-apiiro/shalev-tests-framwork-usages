# Python.PythonPkcs11.json -> "Python PKCS11 Python" [KeyManagementService]
# Expected: import pkcs11
# Envelope-style data keys on an HSM, using the python-pkcs11 object API.
import os
from functools import lru_cache

import pkcs11
from pkcs11 import KeyType, Mechanism, ObjectClass
from pkcs11.exceptions import NoSuchKey

PKCS11_MODULE = os.environ.get("PKCS11_MODULE", "/usr/lib/softhsm/libsofthsm2.so")
TOKEN_LABEL = os.environ.get("PKCS11_TOKEN_LABEL", "app-keys")


@lru_cache(maxsize=1)
def pkcs11_lib():
    return pkcs11.lib(PKCS11_MODULE)


def open_session(pin: str):
    return pkcs11_lib().get_token(token_label=TOKEN_LABEL).open(rw=True, user_pin=pin)


def data_key(session, label: str):
    try:
        return session.get_key(object_class=ObjectClass.SECRET_KEY, key_type=KeyType.AES, label=label)
    except NoSuchKey:
        return session.generate_key(KeyType.AES, 256, label=label, store=True)


def encrypt(pin: str, label: str, plaintext: bytes) -> bytes:
    with open_session(pin) as session:
        iv = session.generate_random(128)
        ciphertext = data_key(session, label).encrypt(plaintext, mechanism=Mechanism.AES_CBC_PAD, mechanism_param=iv)
    return iv + ciphertext


def decrypt(pin: str, label: str, blob: bytes) -> bytes:
    iv, ciphertext = blob[:16], blob[16:]
    with open_session(pin) as session:
        return data_key(session, label).decrypt(ciphertext, mechanism=Mechanism.AES_CBC_PAD, mechanism_param=iv)
