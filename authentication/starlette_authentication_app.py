# Python.StarletteAuthentication.json -> "Starlette Authentication Python" [Authentication]
# Expected: imports starlette.authentication + starlette.middleware.authentication;
#           decorator requires; methods has_required_scope, add_middleware, Middleware
import base64

from starlette.applications import Starlette
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
    has_required_scope,
    requires,
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return None
        try:
            scheme, credentials = conn.headers["Authorization"].split()
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError):
            raise AuthenticationError("Invalid basic auth credentials")
        username, _, _ = decoded.partition(":")
        return AuthCredentials(["authenticated"]), SimpleUser(username)


@requires("authenticated")
async def homepage(request):
    return PlainTextResponse(f"hello {request.user.display_name}")


async def status(request):
    return JSONResponse({"admin": has_required_scope(request, ["admin"])})


app = Starlette(
    routes=[Route("/", homepage), Route("/status", status)],
    middleware=[Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())],
)


def build_app_with_add_middleware():
    other = Starlette(routes=[Route("/", homepage)])
    other.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
    return other
