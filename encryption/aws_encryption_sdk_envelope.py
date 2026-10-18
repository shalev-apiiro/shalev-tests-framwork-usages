# Python.AwsEncryptionSdk.json -> "AWS Encryption SDK Python" [Encryption], vendor AWS
# Expected: import aws_encryption_sdk
import aws_encryption_sdk
from aws_encryption_sdk.identifiers import CommitmentPolicy

client = aws_encryption_sdk.EncryptionSDKClient(
    commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT
)


def encrypt(plaintext: bytes, kms_key_arn: str) -> bytes:
    key_provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(key_ids=[kms_key_arn])
    ciphertext, _header = client.encrypt(source=plaintext, key_provider=key_provider)
    return ciphertext


def decrypt(ciphertext: bytes, kms_key_arn: str) -> bytes:
    key_provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(key_ids=[kms_key_arn])
    plaintext, _header = client.decrypt(source=ciphertext, key_provider=key_provider)
    return plaintext
