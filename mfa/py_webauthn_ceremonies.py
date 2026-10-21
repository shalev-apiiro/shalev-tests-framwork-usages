# Python.PyWebauthn.json -> "Py WebAuthn Python" [MultiFactorAuthentication]
# Expected: import webauthn; methods generate_registration_options, verify_registration_response,
#           generate_authentication_options, verify_authentication_response
# Security-key second factor; the challenge lives in the server-side session between the two calls.
from webauthn import (
    generate_authentication_options,
    generate_registration_options,
    options_to_json,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.helpers import base64url_to_bytes
from webauthn.helpers.exceptions import InvalidAuthenticationResponse, InvalidRegistrationResponse
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

RP_ID = "app.acme.example"
RP_NAME = "Acme Cloud"
ORIGIN = "https://app.acme.example"


def begin_registration(session: dict, user) -> str:
    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=user.webauthn_handle,
        user_name=user.email,
        user_display_name=user.get_full_name(),
        exclude_credentials=[PublicKeyCredentialDescriptor(id=c.credential_id) for c in user.security_keys.all()],
        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=ResidentKeyRequirement.DISCOURAGED,
            user_verification=UserVerificationRequirement.PREFERRED,
        ),
    )
    session["webauthn_registration_challenge"] = options.challenge
    return options_to_json(options)


def finish_registration(session: dict, user, credential_json: str, nickname: str) -> bool:
    try:
        verified = verify_registration_response(
            credential=credential_json,
            expected_challenge=session.pop("webauthn_registration_challenge"),
            expected_rp_id=RP_ID,
            expected_origin=ORIGIN,
        )
    except InvalidRegistrationResponse:
        return False
    user.security_keys.create(
        nickname=nickname,
        credential_id=verified.credential_id,
        public_key=verified.credential_public_key,
        sign_count=verified.sign_count,
    )
    return True


def begin_authentication(session: dict, user) -> str:
    options = generate_authentication_options(
        rp_id=RP_ID,
        allow_credentials=[PublicKeyCredentialDescriptor(id=c.credential_id) for c in user.security_keys.all()],
        user_verification=UserVerificationRequirement.PREFERRED,
    )
    session["webauthn_authentication_challenge"] = options.challenge
    return options_to_json(options)


def finish_authentication(session: dict, user, credential: dict) -> bool:
    key = user.security_keys.filter(credential_id=base64url_to_bytes(credential["rawId"])).first()
    if key is None:
        return False
    try:
        verified = verify_authentication_response(
            credential=credential,
            expected_challenge=session.pop("webauthn_authentication_challenge"),
            expected_rp_id=RP_ID,
            expected_origin=ORIGIN,
            credential_public_key=key.public_key,
            credential_current_sign_count=key.sign_count,
        )
    except InvalidAuthenticationResponse:
        return False
    key.sign_count = verified.new_sign_count
    key.save(update_fields=["sign_count"])
    return True
