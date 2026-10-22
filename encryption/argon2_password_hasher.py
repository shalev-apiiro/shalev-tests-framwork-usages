# Python.Argon2Cffi.json -> "Argon2 Python" [Encryption]
# Expected: import argon2
from dataclasses import dataclass

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

# OWASP-recommended argon2id parameters (19 MiB, 2 iterations, 1 lane)
password_hasher = PasswordHasher(time_cost=2, memory_cost=19 * 1024, parallelism=1)


@dataclass
class Account:
    email: str
    password_hash: str


def set_password(account: Account, password: str) -> None:
    account.password_hash = password_hasher.hash(password)


def check_password(account: Account, password: str, save) -> bool:
    try:
        password_hasher.verify(account.password_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False
    if password_hasher.check_needs_rehash(account.password_hash):
        set_password(account, password)
        save(account)
    return True
