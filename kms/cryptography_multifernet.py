# Python.CryptographyKeyManagement.json -> "Cryptography Key Management Python" [KeyManagementService]
# Expected: method cryptography MultiFernet (key rotation)
# FIELD_ENCRYPTION_KEYS is a comma-separated list of Fernet keys, newest first; older keys stay
# until the rotation job has re-encrypted every stored value.
import os
from functools import lru_cache

from cryptography.fernet import Fernet, InvalidToken, MultiFernet


@lru_cache(maxsize=1)
def keyring() -> MultiFernet:
    keys = [key.strip() for key in os.environ["FIELD_ENCRYPTION_KEYS"].split(",") if key.strip()]
    return MultiFernet([Fernet(key) for key in keys])


def encrypt_field(value: str) -> str:
    return keyring().encrypt(value.encode()).decode()


def decrypt_field(token: str, max_age_seconds: int | None = None) -> str:
    if max_age_seconds is None:
        return keyring().decrypt(token.encode()).decode()
    return keyring().decrypt(token.encode(), ttl=max_age_seconds).decode()


def rotate_field(queryset, field: str) -> int:
    rotated = 0
    for obj in queryset.exclude(**{field: ""}).iterator():
        try:
            setattr(obj, field, keyring().rotate(getattr(obj, field).encode()).decode())
        except InvalidToken:
            continue
        obj.save(update_fields=[field])
        rotated += 1
    return rotated
