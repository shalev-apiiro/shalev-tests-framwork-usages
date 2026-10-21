# Python.StarletteAuthentication.json -> "Starlette Authentication Python" [Authentication]
# Expected: imports starlette.authentication + starlette.middleware.authentication;
#           decorator requires; methods has_required_scope, Middleware
import hashlib

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
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route


class ApiTokenBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        header = conn.headers.get("Authorization")
        if header is None:
            return None
        scheme, _, token = header.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise AuthenticationError("expected a bearer token")

        record = await conn.app.state.api_tokens.find_by_digest(hashlib.sha256(token.encode()).hexdigest())
        if record is None or record.revoked:
            raise AuthenticationError("unknown or revoked token")
        return AuthCredentials(["authenticated", *record.scopes]), SimpleUser(record.owner)


def on_auth_error(conn: HTTPConnection, exc: Exception):
    return PlainTextResponse(str(exc), status_code=401)


@requires("authenticated")
async def list_reports(request):
    rows = await request.app.state.reports.for_owner(request.user.username)
    if has_required_scope(request, ["reports:financials"]):
        return JSONResponse([row.full() for row in rows])
    return JSONResponse([row.summary() for row in rows])


@requires(["authenticated", "reports:write"])
async def create_report(request):
    body = await request.json()
    report = await request.app.state.reports.create(owner=request.user.username, title=body["title"])
    return JSONResponse({"id": report.id}, status_code=201)


def create_app(api_tokens, reports) -> Starlette:
    app = Starlette(
        routes=[
            Route("/reports", list_reports, methods=["GET"]),
            Route("/reports", create_report, methods=["POST"]),
        ],
        middleware=[Middleware(AuthenticationMiddleware, backend=ApiTokenBackend(), on_error=on_auth_error)],
    )
    app.state.api_tokens = api_tokens
    app.state.reports = reports
    return app
