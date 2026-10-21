# Python.CryptographyMfa.json -> "Cryptography MFA Python" [MultiFactorAuthentication]
# Expected: import cryptography.hazmat.primitives.twofactor; methods TOTP, HOTP, get_provisioning_uri
# Second factor for authenticator apps (TOTP) and OATH-HOTP hardware tokens.
import os
import time

from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.hotp import HOTP
from cryptography.hazmat.primitives.twofactor.totp import TOTP

ISSUER = "Acme Cloud"
DIGITS = 6
TIME_STEP = 30
HOTP_LOOK_AHEAD = 10


def enroll_authenticator(email: str) -> tuple[bytes, str]:
    key = os.urandom(20)
    totp = TOTP(key, DIGITS, SHA1(), TIME_STEP)
    return key, totp.get_provisioning_uri(email, ISSUER)


def verify_authenticator_code(key: bytes, code: str, last_used_step: int | None) -> int | None:
    totp = TOTP(key, DIGITS, SHA1(), TIME_STEP)
    now = int(time.time())
    for drift in (0, -TIME_STEP, TIME_STEP):
        step = (now + drift) // TIME_STEP
        if last_used_step is not None and step <= last_used_step:
            continue
        try:
            totp.verify(code.encode(), now + drift)
        except InvalidToken:
            continue
        return step
    return None


def verify_hardware_token(key: bytes, code: str, counter: int) -> int | None:
    hotp = HOTP(key, DIGITS, SHA1())
    for candidate in range(counter, counter + HOTP_LOOK_AHEAD):
        try:
            hotp.verify(code.encode(), candidate)
        except InvalidToken:
            continue
        return candidate + 1
    return None
