# Python.FlaskSession.json -> "Flask Session Python" [SessionManagement]
# Expected: import flask_session, import flask.session, method regenerate
import os
from datetime import timedelta

import redis
from flask import Flask, abort, jsonify, request, session
from flask_session import Session

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ["FLASK_SECRET_KEY"],
    SESSION_TYPE="redis",
    SESSION_REDIS=redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/0")),
    SESSION_KEY_PREFIX="web:session:",
    SESSION_PERMANENT=True,
    PERMANENT_SESSION_LIFETIME=timedelta(hours=12),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
)
Session(app)


def authenticate(email: str, password: str):
    return app.extensions["users"].verify(email, password)


@app.post("/login")
def login():
    user = authenticate(request.form.get("email", ""), request.form.get("password", ""))
    if user is None:
        abort(401)
    app.session_interface.regenerate(session)
    session["user_id"] = user.id
    return jsonify(id=user.id)


@app.post("/logout")
def logout():
    session.clear()
    return "", 204
