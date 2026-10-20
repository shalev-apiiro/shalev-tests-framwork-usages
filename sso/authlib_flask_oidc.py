# Python.AuthlibSSO.json -> "Authlib SSO Python" [SSO]
# Expected: import authlib.integrations.flask_client; methods authorize_redirect,
#           authorize_access_token, parse_id_token
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "change-me"
oauth = OAuth(app)
oauth.register(
    name="okta",
    server_metadata_url="https://example.okta.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@app.route("/login")
def login():
    return oauth.okta.authorize_redirect(url_for("callback", _external=True))


@app.route("/callback")
def callback():
    token = oauth.okta.authorize_access_token()
    session["user"] = oauth.okta.parse_id_token(token, nonce=session.get("nonce"))
    return redirect("/")
