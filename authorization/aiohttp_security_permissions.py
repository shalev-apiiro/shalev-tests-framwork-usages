# Python.AiohttpSecurityAuthorization.json -> "Aiohttp Security Authorization Python" [Authorization]
# Expected: methods check_permission + permits
from aiohttp import web
from aiohttp_security import check_permission, permits


async def edit_document(request):
    await check_permission(request, "documents:edit")
    return web.Response(text="edited")


async def view_document(request):
    if not await permits(request, "documents:view"):
        raise web.HTTPForbidden()
    return web.Response(text="document body")


app = web.Application()
app.add_routes([web.post("/docs/{id}", edit_document), web.get("/docs/{id}", view_document)])
