# Python.Passlib.json -> "Passlib Python" [Encryption]
# Expected: import passlib (passlib.context)
from passlib.context import CryptContext

# New hashes use argon2 (argon2-cffi backend); legacy pbkdf2_sha256 hashes from the old user table still verify
# and are upgraded transparently on the next successful login.
pwd_context = CryptContext(
    schemes=["argon2", "pbkdf2_sha256"],
    deprecated=["pbkdf2_sha256"],
    argon2__memory_cost=19 * 1024,
    argon2__time_cost=2,
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def login(user, password: str, save) -> bool:
    valid, new_hash = pwd_context.verify_and_update(password, user.password_hash)
    if valid and new_hash:
        user.password_hash = new_hash
        save(user)
    return valid
