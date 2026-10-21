# Python.PasslibMfa.json -> "Passlib MFA Python" [MultiFactorAuthentication]
# Expected: import passlib.totp; method to_uri (the factory comes from TOTP.using, so TOTP itself is not called)
import json
import os

from passlib.totp import TOTP, TokenError

# APP_TOTP_SECRETS is a JSON object of {"tag": "secret"} used to encrypt the stored TOTP keys.
TotpFactory = TOTP.using(issuer="Acme Cloud", secrets=json.loads(os.environ["APP_TOTP_SECRETS"]))


def start_enrollment(email: str) -> tuple[str, str]:
    totp = TotpFactory.new()
    return totp.to_json(), totp.to_uri(label=email)


def confirm_code(stored_totp: str, code: str, last_counter: int | None) -> int | None:
    totp = TotpFactory.from_source(stored_totp)
    try:
        match = totp.match(code, last_counter=last_counter)
    except TokenError:
        return None
    return match.counter
