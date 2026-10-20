# Python.PythonPkcs11.json -> "Python PKCS11" [KeyManagementService]
# Expected: import pkcs11
import pkcs11
from pkcs11 import KeyType, Mechanism, ObjectClass

LIB_PATH = "/usr/lib/softhsm/libsofthsm2.so"


def open_session(token_label: str, pin: str):
    lib = pkcs11.lib(LIB_PATH)
    token = lib.get_token(token_label=token_label)
    return token.open(rw=True, user_pin=pin)


def generate_aes_key(session, label: str):
    return session.generate_key(KeyType.AES, 256, label=label, store=True)


def find_key(session, label: str):
    return session.get_key(object_class=ObjectClass.SECRET_KEY, label=label)


def encrypt(session, label: str, plaintext: bytes) -> tuple[bytes, bytes]:
    key = find_key(session, label)
    iv = session.generate_random(128)
    return iv, key.encrypt(plaintext, mechanism=Mechanism.AES_CBC_PAD, mechanism_param=iv)
