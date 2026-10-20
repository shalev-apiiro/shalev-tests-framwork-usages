# Python.Pykcs11.json -> "PyKCS11 Python" [KeyManagementService]
# Expected: import PyKCS11
import PyKCS11

LIB_PATH = "/usr/lib/softhsm/libsofthsm2.so"


def open_session(pin: str):
    lib = PyKCS11.PyKCS11Lib()
    lib.load(LIB_PATH)
    slot = lib.getSlotList(tokenPresent=True)[0]
    session = lib.openSession(slot, PyKCS11.CKF_SERIAL_SESSION | PyKCS11.CKF_RW_SESSION)
    session.login(pin)
    return session


def generate_aes_key(session, label: str):
    template = [
        (PyKCS11.CKA_CLASS, PyKCS11.CKO_SECRET_KEY),
        (PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_AES),
        (PyKCS11.CKA_VALUE_LEN, 32),
        (PyKCS11.CKA_LABEL, label),
        (PyKCS11.CKA_TOKEN, PyKCS11.CK_TRUE),
        (PyKCS11.CKA_ENCRYPT, PyKCS11.CK_TRUE),
        (PyKCS11.CKA_DECRYPT, PyKCS11.CK_TRUE),
    ]
    return session.generateKey(template)


def encrypt(session, key, plaintext: bytes, iv: bytes) -> bytes:
    mechanism = PyKCS11.Mechanism(PyKCS11.CKM_AES_CBC_PAD, iv)
    return bytes(session.encrypt(key, plaintext, mechanism))
