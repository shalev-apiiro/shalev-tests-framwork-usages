# Python.PymongoEncryption.json -> "MongoDB Encryption Python" [Encryption]
# Expected: import pymongo.encryption and pymongo.encryption_options
import base64
import os

from bson.binary import STANDARD
from bson.codec_options import CodecOptions
from pymongo import MongoClient
from pymongo.encryption import Algorithm, ClientEncryption
from pymongo.encryption_options import AutoEncryptionOpts

KEY_VAULT_NAMESPACE = "encryption.__keyVault"
KMS_PROVIDERS = {"local": {"key": base64.b64decode(os.environ["MONGO_LOCAL_MASTER_KEY"])}}
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")


def patients_schema(data_key_id) -> dict:
    deterministic = {"keyId": [data_key_id], "bsonType": "string", "algorithm": Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic}
    return {
        "clinic.patients": {
            "bsonType": "object",
            "encryptMetadata": {"keyId": [data_key_id]},
            "properties": {"ssn": {"encrypt": deterministic}},
        }
    }


def get_or_create_data_key(key_vault_client: MongoClient):
    client_encryption = ClientEncryption(KMS_PROVIDERS, KEY_VAULT_NAMESPACE, key_vault_client, CodecOptions(uuid_representation=STANDARD))
    existing = client_encryption.get_key_by_alt_name("patients")
    return existing["_id"] if existing else client_encryption.create_data_key("local", key_alt_names=["patients"])


def encrypted_client(data_key_id) -> MongoClient:
    opts = AutoEncryptionOpts(KMS_PROVIDERS, KEY_VAULT_NAMESPACE, schema_map=patients_schema(data_key_id))
    return MongoClient(MONGO_URI, auto_encryption_opts=opts)
