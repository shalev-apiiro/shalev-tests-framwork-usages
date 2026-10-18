# Python.OsUrandom.json -> "os.urandom Python" [Encryption]
# Expected: import os, method urandom
import base64
import os


def new_session_key() -> bytes:
    return os.urandom(32)


def new_csrf_token() -> str:
    return base64.urlsafe_b64encode(os.urandom(24)).decode()
