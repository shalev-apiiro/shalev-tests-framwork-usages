# Python.FlaskSession.json -> "Flask Session Python" [SessionManagement]
# Expected: method logout_user, both the bare call and flask_login.logout_user();
# the flask_login import itself stays Flask-Login [Authentication]
import os

import flask_login
from flask import Flask, abort, redirect, render_template_string, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(flask_login.UserMixin):
    def __init__(self, user_id: str, email: str, password_hash: str, active: bool = True):
        self.id, self.email, self.password_hash, self.active = user_id, email, password_hash, active

    @property
    def is_active(self) -> bool:
        return self.active


USERS: dict[str, User] = {}


@login_manager.user_loader
def load_user(user_id: str):
    return USERS.get(user_id)


LOGIN_FORM = """<form method="post"><input name="email"><input name="password" type="password">
<label><input name="remember" type="checkbox"> Remember me</label><button>Sign in</button></form>"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string(LOGIN_FORM)
    user = next((u for u in USERS.values() if u.email == request.form.get("email")), None)
    if user is None or not check_password_hash(user.password_hash, request.form.get("password", "")):
        abort(401)
    login_user(user, remember=request.form.get("remember") == "on")
    return redirect(url_for("dashboard"))


@app.get("/dashboard")
@login_required
def dashboard():
    return f"signed in as {current_user.email}"


@app.post("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.before_request
def drop_deactivated_users():
    if current_user.is_authenticated and not USERS.get(current_user.id, current_user).active:
        flask_login.logout_user()
