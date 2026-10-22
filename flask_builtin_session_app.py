# Python.FlaskSession.json -> "Flask Session Python" [SessionManagement]
# Expected: import flask.session (from flask import session); flask.Flask stays plain Flask [ApiServer]
import os
from datetime import timedelta

from flask import Flask, abort, jsonify, request, session

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ["FLASK_SECRET_KEY"],
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
)

CATALOG = {"sku-100": 1999, "sku-200": 4999}


@app.post("/cart/items")
def add_to_cart():
    sku = request.json.get("sku")
    if sku not in CATALOG:
        abort(404)
    cart = session.setdefault("cart", {})
    cart[sku] = cart.get(sku, 0) + 1
    session.modified = True
    session.permanent = True
    return jsonify(cart=cart)


@app.get("/cart")
def view_cart():
    cart = session.get("cart", {})
    total = sum(CATALOG[sku] * qty for sku, qty in cart.items())
    return jsonify(cart=cart, total_cents=total)


@app.delete("/cart")
def clear_cart():
    session.pop("cart", None)
    return "", 204
