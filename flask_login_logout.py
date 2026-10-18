# Python.FlaskLoginSession.json -> "Flask-Login Session Python" [SessionManagement]
# Expected: method logout_user (both the bare call and flask_login.logout_user());
# the flask_login import itself stays Flask-Login [Authentication]
import flask_login
from flask import Flask
from flask_login import LoginManager, login_required, logout_user

app = Flask(__name__)
login_manager = LoginManager(app)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "logged out"


@app.route("/logout-qualified")
@login_required
def logout_qualified():
    flask_login.logout_user()
    return "logged out"
