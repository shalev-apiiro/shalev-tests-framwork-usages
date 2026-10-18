# Python.DjangoSessions.json -> "Django Sessions Python" [SessionManagement]
# Expected: import django.contrib.sessions..., methods cycle_key, acycle_key, logout, alogout
# (methods are gated on the django.contrib.auth import)
from django.contrib.auth import alogout, authenticate, login, logout
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse


def login_view(request):
    user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
    if user is None:
        return HttpResponse("denied", status=401)
    login(request, user)
    request.session.cycle_key()
    return HttpResponse("logged in")


async def rotate_session_async(request):
    await request.session.acycle_key()
    return HttpResponse("rotated")


def logout_view(request):
    logout(request)
    return HttpResponse("logged out")


async def logout_view_async(request):
    await alogout(request)
    return HttpResponse("logged out")


def new_store():
    return SessionStore()
