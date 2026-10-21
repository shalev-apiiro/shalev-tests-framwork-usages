# Python.Pysaml2.json -> "PySAML2 Python" [SSO]
# Expected: import saml2; methods prepare_for_authenticate + parse_authn_request_response
# Also matches "Flask Session Python" (from flask import session).
import os

from flask import Blueprint, abort, redirect, request, session
from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT
from saml2.client import Saml2Client
from saml2.config import SPConfig
from saml2.response import StatusError
from saml2.validate import ResponseLifetimeExceed

BASE_URL = os.environ["SAML_SP_BASE_URL"]
IDP_ENTITY_ID = os.environ["SAML_IDP_ENTITY_ID"]

SP_SETTINGS = {
    "entityid": f"{BASE_URL}/saml/metadata",
    "key_file": os.environ["SAML_SP_KEY_FILE"],
    "cert_file": os.environ["SAML_SP_CERT_FILE"],
    "service": {
        "sp": {
            "endpoints": {"assertion_consumer_service": [(f"{BASE_URL}/saml/acs", BINDING_HTTP_POST)]},
            "authn_requests_signed": True,
            "want_assertions_signed": True,
            "allow_unsolicited": False,
        }
    },
    "metadata": {"local": [os.environ["SAML_IDP_METADATA_FILE"]]},
}

bp = Blueprint("saml", __name__, url_prefix="/saml")


def saml_client() -> Saml2Client:
    config = SPConfig()
    config.load(SP_SETTINGS)
    return Saml2Client(config=config)


@bp.get("/login")
def login():
    request_id, info = saml_client().prepare_for_authenticate(
        entityid=IDP_ENTITY_ID,
        relay_state=request.args.get("next", "/"),
        binding=BINDING_HTTP_REDIRECT,
    )
    session["saml_outstanding"] = {request_id: request.args.get("next", "/")}
    return redirect(dict(info["headers"])["Location"])


@bp.post("/acs")
def acs():
    outstanding = session.pop("saml_outstanding", {})
    try:
        authn_response = saml_client().parse_authn_request_response(
            request.form["SAMLResponse"], BINDING_HTTP_POST, outstanding
        )
    except (StatusError, ResponseLifetimeExceed):
        abort(401)
    if authn_response is None:
        abort(401)

    identity = authn_response.get_identity()
    session["user"] = {
        "name_id": str(authn_response.name_id.text),
        "email": identity.get("mail", [None])[0],
        "groups": identity.get("memberOf", []),
    }
    return redirect(outstanding.get(authn_response.in_response_to, "/"))
