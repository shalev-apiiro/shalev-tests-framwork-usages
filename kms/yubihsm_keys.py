# Python.PythonYubihsm.json -> "Python YubiHSM" [KeyManagementService]
# Expected: import yubihsm
from yubihsm import YubiHsm
from yubihsm.defs import ALGORITHM, CAPABILITY
from yubihsm.objects import AsymmetricKey

CONNECTOR_URL = "http://localhost:12345"


def open_session(auth_key_id: int, password: str):
    hsm = YubiHsm.connect(CONNECTOR_URL)
    return hsm.create_session_derived(auth_key_id, password)


def generate_signing_key(session, key_id: int, label: str) -> AsymmetricKey:
    return AsymmetricKey.generate(
        session,
        key_id,
        label,
        1,
        CAPABILITY.SIGN_ECDSA,
        ALGORITHM.EC_P256,
    )


def sign(key: AsymmetricKey, payload: bytes) -> bytes:
    return key.sign_ecdsa(payload)


def public_key(key: AsymmetricKey):
    return key.get_public_key()
