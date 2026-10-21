# Python.FlaskSecurityAuthorization.json -> "Flask Security Authorization Python" [Authorization]
# Expected: decorators roles_required, roles_accepted, permissions_required, permissions_accepted;
#           methods has_role + has_permission
# Admin blueprint of a Flask-Security app; Security() and the user datastore are set up in the app factory.
from flask import Blueprint, abort, current_app, jsonify, render_template, request
from flask_security import (
    auth_required,
    current_user,
    permissions_accepted,
    permissions_required,
    roles_accepted,
    roles_required,
)

admin = Blueprint("admin", __name__, url_prefix="/admin")


def datastore():
    return current_app.extensions["security"].datastore


@admin.route("/")
@auth_required()
@roles_accepted("admin", "support")
def index():
    return render_template("admin/index.html", show_billing=current_user.has_permission("billing-read"))


@admin.route("/users")
@auth_required()
@permissions_accepted("user-read", "user-write")
def list_users():
    users = datastore().user_model.query.order_by("email").all()
    return jsonify([{"id": u.id, "email": u.email, "roles": [r.name for r in u.roles]} for u in users])


@admin.route("/users/<int:user_id>/roles", methods=["POST"])
@auth_required()
@permissions_required("user-write")
def grant_role(user_id):
    role = request.json["role"]
    if role == "admin" and not current_user.has_role("admin"):
        abort(403)
    user = datastore().find_user(id=user_id)
    datastore().add_role_to_user(user, role)
    datastore().commit()
    return jsonify({"status": "granted"})


@admin.route("/maintenance", methods=["POST"])
@auth_required()
@roles_required("admin")
def toggle_maintenance():
    current_app.config["MAINTENANCE_MODE"] = request.json["enabled"]
    return jsonify({"maintenance": current_app.config["MAINTENANCE_MODE"]})
