# Python.pymongo.json (extended) -> "MongoDB Python" [DataStorage, Encryption]
# Expected: import pymongo.encryption and pymongo.encryption_options
# (no earlier `from pymongo import MongoClient`: that line would win and keep only DataStorage)
from pymongo.encryption import Algorithm, ClientEncryption
from pymongo.encryption_options import AutoEncryptionOpts

KEY_VAULT_NAMESPACE = "encryption.__keyVault"


def auto_encryption_opts(kms_providers: dict) -> AutoEncryptionOpts:
    return AutoEncryptionOpts(kms_providers, KEY_VAULT_NAMESPACE)


def encrypt_ssn(key_vault_client, kms_providers: dict, data_key_id, ssn: str):
    client_encryption = ClientEncryption(
        kms_providers, KEY_VAULT_NAMESPACE, key_vault_client, key_vault_client.codec_options
    )
    return client_encryption.encrypt(
        ssn, Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic, key_id=data_key_id
    )
