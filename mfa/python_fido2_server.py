# Python.PythonFido2.json -> "Python FIDO2 Python" [MultiFactorAuthentication]
# Expected: import fido2.server; methods register_begin, register_complete,
#           authenticate_begin, authenticate_complete
# Flask blueprint for security-key MFA, shaped like python-fido2's example server.
from fido2.server import Fido2Server
from fido2.webauthn import (
    AttestedCredentialData,
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
    UserVerificationRequirement,
)
from flask import Blueprint, abort, current_app, jsonify, request, session
from flask_login import current_user, login_required

bp = Blueprint("webauthn", __name__, url_prefix="/mfa/webauthn")
server = Fido2Server(PublicKeyCredentialRpEntity(name="Acme Cloud", id="app.acme.example"))


def stored_credentials(user) -> list[AttestedCredentialData]:
    return [AttestedCredentialData(key.credential_data) for key in user.security_keys]


def load_pending_mfa_user():
    user_id = session.get("pending_mfa_user_id")
    user = current_app.extensions["user_store"].get(user_id) if user_id else None
    if user is None:
        abort(401)
    return user


@bp.post("/register/begin")
@login_required
def register_begin():
    options, state = server.register_begin(
        PublicKeyCredentialUserEntity(
            id=current_user.webauthn_handle, name=current_user.email, display_name=current_user.name
        ),
        stored_credentials(current_user),
        user_verification=UserVerificationRequirement.DISCOURAGED,
    )
    session["fido2_state"] = state
    return jsonify(dict(options))


@bp.post("/register/complete")
@login_required
def register_complete():
    auth_data = server.register_complete(session.pop("fido2_state"), request.get_json())
    current_user.add_security_key(bytes(auth_data.credential_data))
    return jsonify({"status": "registered"})


@bp.post("/authenticate/begin")
def authenticate_begin():
    user = load_pending_mfa_user()
    options, state = server.authenticate_begin(stored_credentials(user))
    session["fido2_state"] = state
    return jsonify(dict(options))


@bp.post("/authenticate/complete")
def authenticate_complete():
    user = load_pending_mfa_user()
    server.authenticate_complete(session.pop("fido2_state"), stored_credentials(user), request.get_json())
    session["mfa_verified"] = True
    return jsonify({"status": "verified"})

