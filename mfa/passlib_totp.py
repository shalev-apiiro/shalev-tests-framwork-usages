# Python.PasslibMfa.json -> "Passlib MFA Python" [MultiFactorAuthentication]
# Expected: import passlib.totp; methods TOTP + to_uri
from passlib.totp import TOTP, TokenError

TotpFactory = TOTP.using(issuer="Example App")


def enroll(email: str) -> tuple[str, str]:
    totp = TotpFactory.new()
    return totp.to_json(), totp.to_uri(label=email)


def verify(stored: str, code: str) -> bool:
    totp = TotpFactory.from_json(stored)
    try:
        totp.match(code)
    except TokenError:
        return False
    return True
