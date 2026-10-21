# Python.AuthlibSSO.json -> "Authlib SSO Python" [SSO]
# Expected: import authlib.integrations.flask_client; methods authorize_redirect,
#           authorize_access_token, parse_id_token
# Also matches "Flask Session Python" (from flask import session).
import os
import time

from authlib.integrations.flask_client import OAuth
from flask import Flask, abort, redirect, session, url_for

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["OKTA_CLIENT_ID"] = os.environ["OKTA_CLIENT_ID"]
app.config["OKTA_CLIENT_SECRET"] = os.environ["OKTA_CLIENT_SECRET"]

oauth = OAuth(app)
oauth.register(
    name="okta",
    server_metadata_url=f"{os.environ['OKTA_ISSUER']}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile offline_access"},
)


@app.route("/login")
def login():
    return oauth.okta.authorize_redirect(url_for("callback", _external=True))


@app.route("/oidc/callback")
def callback():
    token = oauth.okta.authorize_access_token()
    userinfo = token["userinfo"]
    if not userinfo.get("email_verified"):
        abort(403)
    session["user"] = {"sub": userinfo["sub"], "email": userinfo["email"], "name": userinfo.get("name")}
    session["refresh_token"] = token.get("refresh_token")
    session["id_token_expires_at"] = userinfo["exp"]
    return redirect(url_for("index"))


@app.before_request
def refresh_identity():
    if "user" not in session or not session.get("refresh_token"):
        return
    if session["id_token_expires_at"] > time.time() + 60:
        return
    token = oauth.okta.fetch_access_token(refresh_token=session["refresh_token"], grant_type="refresh_token")
    claims = oauth.okta.parse_id_token(token, nonce=None)
    if claims["sub"] != session["user"]["sub"]:
        session.clear()
        return redirect(url_for("login"))
    session["id_token_expires_at"] = claims["exp"]
    session["refresh_token"] = token.get("refresh_token", session["refresh_token"])


@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"Signed in as {session['user']['email']}"
