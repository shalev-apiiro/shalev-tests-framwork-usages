# Python.AuthlibSSO.json -> "Authlib SSO Python" [SSO]
# Expected: import authlib.integrations.starlette_client; methods authorize_redirect, authorize_access_token
# Also matches "Starlette Sessions Python" (import starlette.middleware.sessions).
import os

from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.applications import Starlette
from starlette.config import Config
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.routing import Route

config = Config(environ=os.environ)
oauth = OAuth(config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
ALLOWED_DOMAIN = config("GOOGLE_WORKSPACE_DOMAIN")


async def login(request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri, hd=ALLOWED_DOMAIN)


async def auth(request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return PlainTextResponse(f"Sign-in failed: {error.error}", status_code=401)
    userinfo = token["userinfo"]
    if userinfo.get("hd") != ALLOWED_DOMAIN:
        return PlainTextResponse("Use your company account", status_code=403)
    request.session["user"] = {"email": userinfo["email"], "name": userinfo.get("name")}
    return RedirectResponse(url="/")


async def logout(request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")


app = Starlette(
    routes=[
        Route("/login", login),
        Route("/auth", auth, name="auth"),
        Route("/logout", logout, methods=["POST"]),
    ],
    middleware=[Middleware(SessionMiddleware, secret_key=config("SESSION_SECRET"), https_only=True)],
)
