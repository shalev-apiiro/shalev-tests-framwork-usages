# Python.FlaskSecurity.json -> "Flask Security Python" [Authentication]
# Expected: import flask_security; decorators auth_required, auth_token_required,
#           http_auth_required, login_required; method check_and_update_authn_fresh
from datetime import timedelta

from flask import Flask
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    auth_required,
    auth_token_required,
    check_and_update_authn_fresh,
    http_auth_required,
    login_required,
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me"
app.config["SECURITY_PASSWORD_SALT"] = "change-me-too"
db = SQLAlchemy(app)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route("/")
@auth_required()
def home():
    return "session or token"


@app.route("/api/data")
@auth_token_required
def api_data():
    return "token only"


@app.route("/basic")
@http_auth_required
def basic():
    return "http basic auth"


@app.route("/legacy")
@login_required
def legacy():
    return "session login"


@app.route("/settings/password", methods=["POST"])
@auth_required()
def change_password():
    if not check_and_update_authn_fresh(timedelta(minutes=5), timedelta(hours=1)):
        return "re-authentication required", 401
    return "password changed"
