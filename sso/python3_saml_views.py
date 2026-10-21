# Python.Python3Saml.json -> "Python3 SAML Python" [SSO]
# Expected: import onelogin.saml2; methods process_response, process_slo, get_sp_metadata
# Also matches "Flask Session Python" (from flask import session).
import os

from flask import Flask, abort, make_response, redirect, request, session
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
SAML_PATH = os.environ.get("SAML_SETTINGS_PATH", "/etc/acme/saml")


def prepare_flask_request(req):
    return {
        "https": "on" if req.scheme == "https" else "off",
        "http_host": req.host,
        "script_name": req.path,
        "get_data": req.args.copy(),
        "post_data": req.form.copy(),
    }


def init_saml_auth(req) -> OneLogin_Saml2_Auth:
    return OneLogin_Saml2_Auth(prepare_flask_request(req), custom_base_path=SAML_PATH)


@app.route("/saml/login")
def login():
    auth = init_saml_auth(request)
    sso_url = auth.login(return_to=request.args.get("next", "/"))
    session["saml_request_id"] = auth.get_last_request_id()
    return redirect(sso_url)


@app.route("/saml/acs", methods=["POST"])
def acs():
    auth = init_saml_auth(request)
    auth.process_response(request_id=session.pop("saml_request_id", None))
    if auth.get_errors() or not auth.is_authenticated():
        app.logger.warning("SAML ACS rejected: %s", auth.get_last_error_reason())
        abort(401)

    session["saml_user"] = {
        "name_id": auth.get_nameid(),
        "name_id_format": auth.get_nameid_format(),
        "session_index": auth.get_session_index(),
        "attributes": auth.get_attributes(),
    }
    relay_state = request.form.get("RelayState", "/")
    if not relay_state.startswith("/") or relay_state.startswith("//"):
        relay_state = "/"
    return redirect(relay_state)


@app.route("/saml/logout")
def logout():
    auth = init_saml_auth(request)
    user = session.get("saml_user", {})
    return redirect(
        auth.logout(
            return_to="/",
            name_id=user.get("name_id"),
            session_index=user.get("session_index"),
            name_id_format=user.get("name_id_format"),
        )
    )


@app.route("/saml/sls")
def sls():
    auth = init_saml_auth(request)
    url = auth.process_slo(delete_session_cb=session.clear)
    if auth.get_errors():
        abort(400)
    return redirect(url or "/")


@app.route("/saml/metadata")
def metadata():
    settings = OneLogin_Saml2_Settings(custom_base_path=SAML_PATH, sp_validation_only=True)
    sp_metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(sp_metadata)
    if errors:
        return make_response(", ".join(errors), 500)
    response = make_response(sp_metadata, 200)
    response.headers["Content-Type"] = "text/xml"
    return response
