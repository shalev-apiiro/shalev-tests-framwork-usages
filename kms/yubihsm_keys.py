# Python.PythonYubihsm.json -> "Python YubiHSM Python" [KeyManagementService]
# Expected: import yubihsm
# Release-signing key that never leaves the YubiHSM 2; the connector runs next to the build agent.
import os
from contextlib import contextmanager

from yubihsm import YubiHsm
from yubihsm.defs import ALGORITHM, CAPABILITY, OBJECT
from yubihsm.exceptions import YubiHsmDeviceError
from yubihsm.objects import AsymmetricKey

CONNECTOR_URL = os.environ.get("YUBIHSM_CONNECTOR_URL", "http://127.0.0.1:12345")
AUTH_KEY_ID = int(os.environ.get("YUBIHSM_AUTH_KEY_ID", "1"))
SIGNING_KEY_ID = 0x0100
SIGNING_DOMAINS = 1


@contextmanager
def hsm_session(password: str):
    hsm = YubiHsm.connect(CONNECTOR_URL)
    session = hsm.create_session_derived(AUTH_KEY_ID, password)
    try:
        yield session
    finally:
        session.close()
        hsm.close()


def ensure_signing_key(session) -> AsymmetricKey:
    key = session.get_object(SIGNING_KEY_ID, OBJECT.ASYMMETRIC_KEY)
    try:
        key.get_info()
        return key
    except YubiHsmDeviceError:
        return AsymmetricKey.generate(
            session, SIGNING_KEY_ID, "release-signing", SIGNING_DOMAINS, CAPABILITY.SIGN_ECDSA, ALGORITHM.EC_P256
        )


def sign_release(password: str, artifact: bytes) -> tuple[bytes, object]:
    with hsm_session(password) as session:
        key = ensure_signing_key(session)
        return key.sign_ecdsa(artifact), key.get_public_key()
