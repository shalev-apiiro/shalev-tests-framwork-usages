# Python.SqlalchemyUtils.json -> "SQLAlchemy-Utils Python" [Encryption]
# Expected: import sqlalchemy_utils.StringEncryptedType and sqlalchemy_utils.types.encrypted...
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
