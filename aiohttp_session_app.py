# Python.AiohttpSession.json -> "aiohttp-session Python" [SessionManagement]
# Expected: import aiohttp_session, methods new_session + invalidate
from aiohttp import web
from aiohttp_session import get_session, new_session


async def login(request):
    session = await new_session(request)
    session["user"] = "alice"
    return web.Response(text="logged in")


async def logout(request):
    session = await get_session(request)
    session.invalidate()
    return web.Response(text="logged out")


app = web.Application()
app.add_routes([web.post("/login", login), web.post("/logout", logout)])
