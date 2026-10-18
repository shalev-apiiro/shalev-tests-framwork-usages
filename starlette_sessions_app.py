# Python.StarletteSessionMiddleware.json -> "Starlette Sessions Python" [SessionManagement]
# Expected: import starlette.middleware.sessions (FastAPI apps import it from Starlette)
import os

from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.environ["SESSION_SECRET"])


@app.get("/visit")
async def visit(request: Request):
    request.session["visits"] = request.session.get("visits", 0) + 1
    return {"visits": request.session["visits"]}
