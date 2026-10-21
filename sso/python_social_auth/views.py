# Python.PythonSocialAuth.json -> "Python Social Auth Python" [SSO]
# Expected: imports social_core + social_django; methods do_auth, do_complete; decorator psa
# Replaces social_django's begin/complete views so sign-in is audited, and adds a token exchange
# endpoint for the mobile app.
import logging

from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from social_core.actions import do_auth, do_complete
from social_core.exceptions import AuthException
from social_django.utils import psa

audit_log = logging.getLogger("audit.sso")


def _login(backend, user, social_user):
    user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
    login(backend.strategy.request, user)
    audit_log.info("social login user=%s provider=%s", user.pk, backend.name)


@never_cache
@psa("social:complete")
def begin(request, backend):
    return do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)


@never_cache
@csrf_exempt
@psa("social:complete")
def complete(request, backend, *args, **kwargs):
    return do_complete(request.backend, _login, user=request.user, redirect_name=REDIRECT_FIELD_NAME, request=request)


@csrf_exempt
@require_POST
@psa("social:complete")
def exchange_token(request, backend):
    try:
        user = request.backend.do_auth(request.POST["access_token"])
    except (KeyError, AuthException):
        user = None
    if user is None or not user.is_active:
        return JsonResponse({"error": "authentication failed"}, status=401)
    _login(request.backend, user, None)
    return JsonResponse({"username": user.get_username()})
