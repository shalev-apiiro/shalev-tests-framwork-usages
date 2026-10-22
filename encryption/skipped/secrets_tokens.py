# NEGATIVE SAMPLE: secrets (std-lib) (row 54) was deliberately skipped in apiiro/lim PR #53633,
# so this file must NOT be detected as an Encryption control.
# Expected: no framework usage detected
import secrets
import string


def api_key() -> str:
    return secrets.token_urlsafe(32)


def reset_token() -> str:
    return secrets.token_hex(16)


def aes_key() -> bytes:
    return secrets.token_bytes(32)


def otp_code() -> str:
    return f"{secrets.randbelow(10**6):06d}"


def request_id() -> int:
    return secrets.randbits(64)


def temp_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def shuffle_secure(items: list) -> list:
    rng = secrets.SystemRandom()
    rng.shuffle(items)
    return items
