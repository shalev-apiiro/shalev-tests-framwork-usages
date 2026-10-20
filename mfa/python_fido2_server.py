# Python.PythonFido2.json -> "Python FIDO2 Python" [MultiFactorAuthentication]
# Expected: import fido2.server; methods register_begin, register_complete,
#           authenticate_begin, authenticate_complete
from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity, PublicKeyCredentialUserEntity, UserVerificationRequirement

rp = PublicKeyCredentialRpEntity(name="Example App", id="example.com")
server = Fido2Server(rp)


def begin_registration(user_id: bytes, username: str):
    user = PublicKeyCredentialUserEntity(id=user_id, name=username, display_name=username)
    options, state = server.register_begin(user, user_verification=UserVerificationRequirement.PREFERRED)
    return options, state


def finish_registration(state, response):
    auth_data = server.register_complete(state, response)
    return auth_data.credential_data


def begin_authentication(credentials):
    options, state = server.authenticate_begin(credentials)
    return options, state


def finish_authentication(state, credentials, response):
    return server.authenticate_complete(state, credentials, response)
