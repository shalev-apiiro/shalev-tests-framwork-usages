# Python.StarletteSessionMiddleware.json -> "Starlette Sessions Python" [SessionManagement]
# Expected: import starlette.middleware.sessions (FastAPI apps import it from Starlette)
import os

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SESSION_SECRET"],
    session_cookie="sid",
    max_age=8 * 3600,
    same_site="lax",
    https_only=True,
)


class Credentials(BaseModel):
    email: str
    password: str


def current_user_id(request: Request) -> int:
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401)
    return user_id


@app.post("/login")
async def login(credentials: Credentials, request: Request):
    user = await request.app.state.users.verify(credentials.email, credentials.password)
    if user is None:
        raise HTTPException(status_code=401, detail="invalid credentials")
    request.session.clear()
    request.session["user_id"] = user.id
    return {"id": user.id}


@app.get("/me")
async def me(user_id: int = Depends(current_user_id)):
    return {"id": user_id}


@app.post("/logout", status_code=204)
async def logout(request: Request):
    request.session.clear()
