# Python.QuartAuth.json -> "Quart Auth Python" [Authentication]
# Expected: import quart_auth; decorators login_required + basic_auth_required
from quart import Quart
from quart_auth import AuthUser, QuartAuth, basic_auth_required, login_required, login_user

app = Quart(__name__)
app.secret_key = "change-me"
app.config["QUART_AUTH_BASIC_USERNAME"] = "admin"
app.config["QUART_AUTH_BASIC_PASSWORD"] = "change-me"
QuartAuth(app)


@app.post("/login")
async def login():
    login_user(AuthUser("alice"))
    return "logged in"


@app.get("/profile")
@login_required
async def profile():
    return "cookie-authenticated users only"


@app.get("/admin")
@basic_auth_required()
async def admin():
    return "http basic auth"
