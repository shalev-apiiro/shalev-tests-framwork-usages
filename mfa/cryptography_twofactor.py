# Python.CryptographyMfa.json -> "Cryptography MFA Python" [MultiFactorAuthentication]
# Expected: import cryptography.hazmat.primitives.twofactor; methods TOTP, HOTP, get_provisioning_uri
import os
import time

from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.hotp import HOTP
from cryptography.hazmat.primitives.twofactor.totp import TOTP


def enroll(account: str) -> tuple[bytes, str]:
    key = os.urandom(20)
    totp = TOTP(key, 6, SHA1(), 30)
    return key, totp.get_provisioning_uri(account, "Example App")


def verify_totp(key: bytes, code: bytes) -> bool:
    totp = TOTP(key, 6, SHA1(), 30)
    try:
        totp.verify(code, int(time.time()))
    except InvalidToken:
        return False
    return True


def verify_hotp(key: bytes, code: bytes, counter: int) -> bool:
    hotp = HOTP(key, 6, SHA1())
    try:
        hotp.verify(code, counter)
    except InvalidToken:
        return False
    return True
