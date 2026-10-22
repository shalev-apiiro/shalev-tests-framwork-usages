# Python.WerkzeugSecurity.json -> "Werkzeug Security Python" [Encryption]
# Expected: import werkzeug.security.generate_password_hash / check_password_hash
import os

from flask import Flask, abort, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]

USERS: dict[str, str] = {}


@app.post("/signup")
def signup():
    email, password = request.json.get("email", "").lower(), request.json.get("password", "")
    if len(password) < 12 or email in USERS:
        abort(400)
    USERS[email] = generate_password_hash(password, method="scrypt")
    return jsonify(email=email), 201


@app.post("/login")
def login():
    email, password = request.json.get("email", "").lower(), request.json.get("password", "")
    stored = USERS.get(email)
    if stored is None or not check_password_hash(stored, password):
        abort(401)
    return jsonify(email=email)
