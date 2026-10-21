# Python.QuartAuth.json -> "Quart Auth Python" [Authentication]
# Expected: import quart_auth; decorators login_required + basic_auth_required
import os

from quart import Quart, current_app, redirect, render_template, request, url_for
from quart_auth import (
    AuthUser,
    QuartAuth,
    Unauthorized,
    basic_auth_required,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash

app = Quart(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["QUART_AUTH_COOKIE_SECURE"] = True
app.config["QUART_AUTH_BASIC_USERNAME"] = os.environ["OPS_USERNAME"]
app.config["QUART_AUTH_BASIC_PASSWORD"] = os.environ["OPS_PASSWORD"]
QuartAuth(app)


def store():
    return current_app.extensions["store"]


@app.errorhandler(Unauthorized)
async def redirect_to_login(*_):
    return redirect(url_for("login", next=request.path))


@app.route("/login", methods=["GET", "POST"])
async def login():
    if request.method == "GET":
        return await render_template("login.html")
    form = await request.form
    user = await store().get_user_by_email(form["email"])
    if user is None or not check_password_hash(user.password_hash, form["password"]):
        return await render_template("login.html", error="Invalid email or password"), 401
    login_user(AuthUser(str(user.id)), remember=form.get("remember") == "on")
    return redirect(request.args.get("next", url_for("orders")))


@app.post("/logout")
@login_required
async def logout():
    logout_user()
    return redirect(url_for("login"))


@app.get("/orders")
@login_required
async def orders():
    return await render_template("orders.html", orders=await store().list_orders(int(current_user.auth_id)))


@app.get("/ops/queues")
@basic_auth_required()
async def ops_queues():
    return await store().queue_stats()
