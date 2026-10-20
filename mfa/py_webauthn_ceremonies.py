# Python.PyWebauthn.json -> "Py WebAuthn Python" [MultiFactorAuthentication]
# Expected: import webauthn; methods generate_registration_options, verify_registration_response,
#           generate_authentication_options, verify_authentication_response
from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    options_to_json,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.helpers.structs import PublicKeyCredentialDescriptor, UserVerificationRequirement

RP_ID = "example.com"
ORIGIN = "https://example.com"


def begin_registration(user_id: bytes, username: str) -> str:
    options = generate_registration_options(rp_id=RP_ID, rp_name="Example", user_id=user_id, user_name=username)
    return options_to_json(options)


def finish_registration(credential: dict, challenge: bytes):
    return verify_registration_response(
        credential=credential, expected_challenge=challenge, expected_rp_id=RP_ID, expected_origin=ORIGIN
    )


def begin_authentication(credential_ids: list[bytes]) -> str:
    options = generate_authentication_options(
        rp_id=RP_ID,
        allow_credentials=[PublicKeyCredentialDescriptor(id=cid) for cid in credential_ids],
        user_verification=UserVerificationRequirement.PREFERRED,
    )
    return options_to_json(options)


def finish_authentication(credential: dict, challenge: bytes, public_key: bytes, sign_count: int):
    return verify_authentication_response(
        credential=credential,
        expected_challenge=challenge,
        expected_rp_id=RP_ID,
        expected_origin=ORIGIN,
        credential_public_key=public_key,
        credential_current_sign_count=sign_count,
    )
