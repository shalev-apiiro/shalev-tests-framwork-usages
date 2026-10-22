# Python.AwsEncryptionSdk.json -> "AWS Encryption SDK Python" [Encryption], vendor AWS
# Expected: import aws_encryption_sdk
import os

import aws_encryption_sdk
from aws_encryption_sdk.identifiers import CommitmentPolicy

KMS_KEY_ARN = os.environ["DOCUMENTS_KMS_KEY_ARN"]

client = aws_encryption_sdk.EncryptionSDKClient(commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT)
key_provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(key_ids=[KMS_KEY_ARN])


def encrypt_document(tenant_id: str, document_id: str, body: bytes) -> bytes:
    context = {"tenant_id": tenant_id, "document_id": document_id, "purpose": "customer-document"}
    ciphertext, _header = client.encrypt(source=body, key_provider=key_provider, encryption_context=context)
    return ciphertext


def decrypt_document(tenant_id: str, document_id: str, ciphertext: bytes) -> bytes:
    plaintext, header = client.decrypt(source=ciphertext, key_provider=key_provider)
    if header.encryption_context.get("tenant_id") != tenant_id or header.encryption_context.get("document_id") != document_id:
        raise PermissionError("encryption context does not match the requested document")
    return plaintext
