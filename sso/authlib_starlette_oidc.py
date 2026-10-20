# Python.AuthlibSSO.json -> "Authlib SSO Python" [SSO]
# Expected: import authlib.integrations.starlette_client; methods authorize_redirect, authorize_access_token
from authlib.integrations.starlette_client import OAuth
from starlette.applications import Starlette
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from starlette.routing import Route

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


async def login(request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


async def auth(request):
    token = await oauth.google.authorize_access_token(request)
    request.session["user"] = dict(token["userinfo"])
    return RedirectResponse(url="/")


app = Starlette(routes=[Route("/login", login), Route("/auth", auth, name="auth")])
app.add_middleware(SessionMiddleware, secret_key="change-me")
