# Python.RandomSystemRandom.json -> "random.SystemRandom Python" [Encryption]
# Expected: import random, method SystemRandom
import random
import string

rng = random.SystemRandom()


def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(rng.choice(alphabet) for _ in range(length))
