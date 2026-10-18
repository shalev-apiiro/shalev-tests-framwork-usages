# Python.Bcrypt.json -> "Bcrypt Python" [Encryption]
# Expected: import bcrypt
import bcrypt


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))


def verify_password(password: str, stored_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), stored_hash)
