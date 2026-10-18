# Python.Passlib.json -> "Passlib Python" [Encryption]
# Expected: import passlib (passlib.context, passlib.hash)
from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    return pwd_context.verify(password, stored_hash)


def legacy_hash(password: str) -> str:
    return pbkdf2_sha256.hash(password)
