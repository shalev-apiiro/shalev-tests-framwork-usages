# Python.DjangoAllauth.json -> "Django Allauth Python" [Authentication]
# Expected: import allauth.headless.contrib.ninja.security
# django-ninja flavour of the same SPA API, authenticated by the allauth headless session token.
from allauth.headless.contrib.ninja.security import x_session_token_auth
from ninja import NinjaAPI, Schema

api = NinjaAPI(auth=x_session_token_auth, urls_namespace="spa-api")


class ProfileOut(Schema):
    email: str
    first_name: str
    last_name: str


class ProjectOut(Schema):
    id: int
    name: str


@api.get("/profile", response=ProfileOut)
def profile(request):
    return request.user


@api.get("/projects", response=list[ProjectOut])
def projects(request):
    return request.user.projects.order_by("name")
