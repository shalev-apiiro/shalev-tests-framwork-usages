# Python.FlaskSecurity.json -> "Flask Security Python" [Authentication]
# Expected: import flask_security; decorators auth_required, auth_token_required, http_auth_required;
#           method check_and_update_authn_fresh
import os
from datetime import timedelta

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    auth_required,
    auth_token_required,
    check_and_update_authn_fresh,
    current_user,
    http_auth_required,
)
from flask_security.models import fsqla_v3 as fsqla
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SECURITY_PASSWORD_SALT"] = os.environ["SECURITY_PASSWORD_SALT"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SECURITY_TOKEN_MAX_AGE"] = 3600

db = SQLAlchemy(app)
fsqla.FsModels.set_db_info(db)


class Role(db.Model, fsqla.FsRoleMixin):
    pass


class User(db.Model, fsqla.FsUserMixin):
    pass


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route("/")
@auth_required()
def dashboard():
    projects = Project.query.filter_by(owner_id=current_user.id).all()
    return render_template("dashboard.html", projects=projects)


@app.route("/api/v1/projects")
@auth_token_required
def api_projects():
    projects = Project.query.filter_by(owner_id=current_user.id).all()
    return jsonify([{"id": p.id, "name": p.name} for p in projects])


@app.route("/metrics")
@http_auth_required
def metrics():
    return {"users": User.query.count(), "projects": Project.query.count()}


@app.route("/account/delete", methods=["POST"])
@auth_required()
def delete_account():
    if not check_and_update_authn_fresh(timedelta(minutes=10), timedelta(minutes=1)):
        return redirect(url_for("security.verify", next=request.path))
    user_datastore.delete_user(current_user)
    db.session.commit()
    return redirect(url_for("security.login"))
