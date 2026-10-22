# NEGATIVE SAMPLE: os.urandom (row 35) was deliberately skipped in apiiro/lim PR #53633,
# so this file must NOT be detected as an Encryption control.
# Expected: no framework usage detected
import base64
import os


def new_session_key() -> bytes:
    return os.urandom(32)


def new_csrf_token() -> str:
    return base64.urlsafe_b64encode(os.urandom(24)).decode()
