# Python.AiohttpSecurityAuthorization.json -> "Aiohttp Security Authorization Python" [Authorization]
# Expected: methods check_permission + permits
# Document handlers of an aiohttp app whose security policy is set up in its app factory.
from aiohttp import web
from aiohttp_security import authorized_userid, check_permission, permits

routes = web.RouteTableDef()


@routes.get("/documents/{doc_id}")
async def view_document(request: web.Request) -> web.Response:
    await check_permission(request, "documents:read")
    document = await request.app["documents"].get(request.match_info["doc_id"])
    if document is None:
        raise web.HTTPNotFound()
    return web.json_response(
        {
            "id": document["id"],
            "title": document["title"],
            "body": document["body"],
            "can_edit": await permits(request, "documents:write", context=document),
        }
    )


@routes.put("/documents/{doc_id}")
async def update_document(request: web.Request) -> web.Response:
    document = await request.app["documents"].get(request.match_info["doc_id"])
    if document is None:
        raise web.HTTPNotFound()
    await check_permission(request, "documents:write", context=document)
    body = await request.json()
    await request.app["documents"].update(document["id"], title=body["title"], body=body["body"])
    return web.json_response({"status": "updated"})


@routes.delete("/documents/{doc_id}")
async def delete_document(request: web.Request) -> web.Response:
    await check_permission(request, "documents:delete")
    await request.app["documents"].delete(
        request.match_info["doc_id"], deleted_by=await authorized_userid(request)
    )
    return web.Response(status=204)
