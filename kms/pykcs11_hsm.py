# Python.Pykcs11.json -> "PyKCS11 Python" [KeyManagementService]
# Expected: import PyKCS11
# Data-encryption keys kept on an HSM (SoftHSM in development) and used through the PKCS#11 API.
import os
from contextlib import contextmanager

import PyKCS11

PKCS11_MODULE = os.environ.get("PKCS11_MODULE", "/usr/lib/softhsm/libsofthsm2.so")
TOKEN_LABEL = os.environ.get("PKCS11_TOKEN_LABEL", "app-keys")


@contextmanager
def hsm_session(pin: str):
    lib = PyKCS11.PyKCS11Lib()
    lib.load(PKCS11_MODULE)
    slot = next(
        slot for slot in lib.getSlotList(tokenPresent=True) if lib.getTokenInfo(slot).label.strip() == TOKEN_LABEL
    )
    session = lib.openSession(slot, PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)
    session.login(pin)
    try:
        yield session
    finally:
        session.logout()
        session.closeSession()


def find_or_create_aes_key(session, label: str):
    existing = session.findObjects([(PyKCS11.CKA_CLASS, PyKCS11.CKO_SECRET_KEY), (PyKCS11.CKA_LABEL, label)])
    if existing:
        return existing[0]
    return session.generateKey(
        [
            (PyKCS11.CKA_CLASS, PyKCS11.CKO_SECRET_KEY),
            (PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_AES),
            (PyKCS11.CKA_VALUE_LEN, 32),
            (PyKCS11.CKA_LABEL, label),
            (PyKCS11.CKA_TOKEN, PyKCS11.CK_TRUE),
            (PyKCS11.CKA_SENSITIVE, PyKCS11.CK_TRUE),
            (PyKCS11.CKA_EXTRACTABLE, PyKCS11.CK_FALSE),
            (PyKCS11.CKA_ENCRYPT, PyKCS11.CK_TRUE),
            (PyKCS11.CKA_DECRYPT, PyKCS11.CK_TRUE),
        ],
        PyKCS11.MechanismAESGENERATEKEY,
    )


def encrypt(session, key, plaintext: bytes) -> bytes:
    iv = bytes(session.generateRandom(16))
    ciphertext = bytes(session.encrypt(key, plaintext, PyKCS11.Mechanism(PyKCS11.CKM_AES_CBC_PAD, iv)))
    return iv + ciphertext


def decrypt(session, key, blob: bytes) -> bytes:
    iv, ciphertext = blob[:16], blob[16:]
    return bytes(session.decrypt(key, ciphertext, PyKCS11.Mechanism(PyKCS11.CKM_AES_CBC_PAD, iv)))
