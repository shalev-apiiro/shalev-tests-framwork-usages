# Python.Pyotp.json -> "PyOTP Python" [MultiFactorAuthentication]
# Expected: import pyotp; methods TOTP, HOTP, random_base32, random_hex, provisioning_uri
import pyotp


def enroll(email: str) -> tuple[str, str]:
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    return secret, totp.provisioning_uri(name=email, issuer_name="Example App")


def verify_totp(secret: str, code: str) -> bool:
    return pyotp.TOTP(secret).verify(code, valid_window=1)


def enroll_counter_based() -> str:
    return pyotp.random_hex()


def verify_hotp(secret: str, code: str, counter: int) -> bool:
    return pyotp.HOTP(secret).verify(code, counter)
