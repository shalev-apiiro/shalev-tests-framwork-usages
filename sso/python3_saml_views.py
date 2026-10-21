# Python.Python3Saml.json -> "Python3 SAML Python" [SSO]
# Expected: import onelogin.saml2; methods process_response, process_slo, get_sp_metadata
from flask import Flask, make_response, redirect, request, session
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings

app = Flask(__name__)
app.secret_key = "change-me"
SAML_PATH = "/etc/saml"


def prepare_request(req):
    return {
        "https": "on" if req.scheme == "https" else "off",
        "http_host": req.host,
        "script_name": req.path,
        "get_data": req.args.copy(),
        "post_data": req.form.copy(),
    }


@app.route("/saml/acs", methods=["POST"])
def acs():
    auth = OneLogin_Saml2_Auth(prepare_request(request), custom_base_path=SAML_PATH)
    auth.process_response()
    if auth.get_errors():
        return "SAML error", 401
    session["user"] = auth.get_nameid()
    return redirect("/")


@app.route("/saml/sls")
def sls():
    auth = OneLogin_Saml2_Auth(prepare_request(request), custom_base_path=SAML_PATH)
    url = auth.process_slo(delete_session_cb=session.clear)
    return redirect(url or "/")


@app.route("/saml/metadata")
def metadata():
    settings = OneLogin_Saml2_Settings(custom_base_path=SAML_PATH, sp_validation_only=True)
    response = make_response(settings.get_sp_metadata(), 200)
    response.headers["Content-Type"] = "text/xml"
    return response
