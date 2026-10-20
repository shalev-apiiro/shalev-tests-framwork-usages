# Python.AiohttpSecurity.json -> "Aiohttp Security Python" [Authentication]
# Expected: methods setup_security (aiohttp_security.setup alias) + check_authorized
from aiohttp import web
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy, check_authorized
from aiohttp_security.abc import AbstractAuthorizationPolicy


class DictAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, users):
        self.users = users

    async def authorized_userid(self, identity):
        return identity if identity in self.users else None

    async def permits(self, identity, permission, context=None):
        return permission in self.users.get(identity, ())


async def profile(request):
    user_id = await check_authorized(request)
    return web.Response(text=f"hello {user_id}")


def make_app():
    app = web.Application()
    setup_security(app, SessionIdentityPolicy(), DictAuthorizationPolicy({"alice": {"view"}}))
    app.add_routes([web.get("/profile", profile)])
    return app
