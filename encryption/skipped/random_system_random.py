# NEGATIVE SAMPLE: random.SystemRandom (row 53) was deliberately skipped in apiiro/lim PR #53633,
# so this file must NOT be detected as an Encryption control.
# Expected: no framework usage detected
import random
import string

rng = random.SystemRandom()


def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(rng.choice(alphabet) for _ in range(length))
