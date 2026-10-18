# Python.FlaskSession.json -> "Flask-Session Python" [SessionManagement]
# Expected: import flask_session, method regenerate
from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/login", methods=["POST"])
def login():
    app.session_interface.regenerate(session)
    session["user"] = "alice"
    return "logged in"
