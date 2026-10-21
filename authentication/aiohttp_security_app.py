# Python.AiohttpSecurity.json -> "Aiohttp Security Python" [Authentication]
# Expected: methods setup_security (aiohttp_security.setup alias) + check_authorized
# Also matches "aiohttp-session Python" (import aiohttp_session) because the identity is kept in the session.
import base64
import hashlib
import hmac
import os

from aiohttp import web
from aiohttp_security import SessionIdentityPolicy, check_authorized, forget, remember
from aiohttp_security import setup as setup_security
from aiohttp_security.abc import AbstractAuthorizationPolicy
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage


def hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)


class DbAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, db):
        self.db = db

    async def authorized_userid(self, identity):
        user = await self.db.fetch_user(identity)
        if user is None or user["disabled"]:
            return None
        return identity

    async def permits(self, identity, permission, context=None):
        user = await self.db.fetch_user(identity)
        return user is not None and permission in user["permissions"]


async def login(request: web.Request) -> web.Response:
    form = await request.post()
    user = await request.app["db"].fetch_user(form.get("username", ""))
    if user is None or not hmac.compare_digest(
        hash_password(form.get("password", ""), user["salt"]), user["password_hash"]
    ):
        raise web.HTTPUnauthorized(text="invalid username or password")

    response = web.HTTPFound("/account")
    await remember(request, response, user["username"])
    raise response


async def logout(request: web.Request) -> web.Response:
    await check_authorized(request)
    response = web.HTTPFound("/")
    await forget(request, response)
    raise response


async def account(request: web.Request) -> web.Response:
    username = await check_authorized(request)
    user = await request.app["db"].fetch_user(username)
    return web.json_response({"username": username, "email": user["email"]})


def create_app(db) -> web.Application:
    app = web.Application()
    app["db"] = db

    secret_key = base64.urlsafe_b64decode(os.environ["SESSION_SECRET_KEY"])
    setup_session(app, EncryptedCookieStorage(secret_key, cookie_name="sid", secure=True, httponly=True))
    setup_security(app, SessionIdentityPolicy(), DbAuthorizationPolicy(db))

    app.add_routes(
        [
            web.post("/login", login),
            web.post("/logout", logout),
            web.get("/account", account),
        ]
    )
    return app
