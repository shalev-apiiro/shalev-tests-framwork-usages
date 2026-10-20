# Python.FlaskSecurityAuthorization.json -> "Flask Security Authorization Python" [Authorization]
# Expected: decorators roles_required, roles_accepted, permissions_required, permissions_accepted;
#           methods has_role + has_permission
from flask import Flask, abort
from flask_security import (
    current_user,
    permissions_accepted,
    permissions_required,
    roles_accepted,
    roles_required,
)

app = Flask(__name__)


@app.route("/admin")
@roles_required("admin")
def admin_panel():
    return "admins only"


@app.route("/reports")
@roles_accepted("admin", "auditor")
def reports():
    return "admins or auditors"


@app.route("/users", methods=["POST"])
@permissions_required("user-write")
def create_user():
    return "created"


@app.route("/users")
@permissions_accepted("user-read", "user-write")
def list_users():
    return "users"


@app.route("/billing")
def billing():
    if not current_user.has_role("billing") and not current_user.has_permission("billing-read"):
        abort(403)
    return "billing"
