# Python.FlaskBuiltInSession.json -> "Flask Session Python" [SessionManagement]
# Expected: import flask.session (from flask import session); flask.Flask stays plain Flask [ApiServer]
from flask import Flask, session

app = Flask(__name__)


@app.route("/remember")
def remember():
    session["theme"] = "dark"
    return "ok"


@app.route("/forget")
def forget():
    session.clear()
    return "ok"
