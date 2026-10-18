# Python.werkzeug.json (extended) -> "Werkzeug Python" [ApiServer, Encryption]
# Expected: import werkzeug.security.generate_password_hash / check_password_hash
from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(password: str) -> str:
    return generate_password_hash(password, method="scrypt")


def verify_password(stored_hash: str, password: str) -> bool:
    return check_password_hash(stored_hash, password)
