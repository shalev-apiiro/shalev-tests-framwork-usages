# NEGATIVE SAMPLE: SQLAlchemy-Utils encrypted types (row 56) was deliberately skipped in apiiro/lim PR #53633,
# so this file must NOT be detected as an Encryption control.
# Expected: no framework usage detected
import os

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

Base = declarative_base()


def field_key() -> str:
    return os.environ["FIELD_ENCRYPTION_KEY"]


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    ssn = Column(StringEncryptedType(key=field_key, engine=AesEngine, padding="pkcs5"))
