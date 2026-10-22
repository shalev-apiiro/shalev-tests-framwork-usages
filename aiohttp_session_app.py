# Python.AiohttpSession.json -> "Aiohttp Session Python" [SessionManagement]
# Expected: import aiohttp_session; methods new_session, get_session, invalidate
import base64
import os

from aiohttp import web
from aiohttp_session import get_session, new_session, setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

routes = web.RouteTableDef()


@routes.post("/login")
async def login(request: web.Request) -> web.Response:
    form = await request.post()
    user = await request.app["users"].authenticate(form.get("username", ""), form.get("password", ""))
    if user is None:
        raise web.HTTPUnauthorized(text="invalid credentials")
    session = await new_session(request)
    session["user_id"] = user.id
    return web.json_response({"id": user.id})


@routes.get("/me")
async def me(request: web.Request) -> web.Response:
    session = await get_session(request)
    if "user_id" not in session:
        raise web.HTTPUnauthorized()
    return web.json_response({"id": session["user_id"]})


@routes.post("/logout")
async def logout(request: web.Request) -> web.Response:
    session = await get_session(request)
    session.invalidate()
    raise web.HTTPNoContent()


def create_app(users) -> web.Application:
    app = web.Application()
    app["users"] = users
    secret_key = base64.urlsafe_b64decode(os.environ["SESSION_KEY"])
    setup(app, EncryptedCookieStorage(secret_key, cookie_name="sid", max_age=8 * 3600, secure=True, httponly=True, samesite="Lax"))
    app.add_routes(routes)
    return app
