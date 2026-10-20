# Python.PythonSocialAuth.json -> "Python Social Auth Python" [SSO]
# Expected: imports social_core + social_django; methods do_auth, do_complete, auth_complete,
#           load_strategy; decorator psa
from django.contrib.auth import login
from django.http import JsonResponse
from social_core.actions import do_auth, do_complete
from social_core.backends.oauth import BaseOAuth2
from social_django.utils import load_backend, load_strategy, psa


class CompanyOAuth2(BaseOAuth2):
    name = "company"
    AUTHORIZATION_URL = "https://idp.example.com/oauth/authorize"
    ACCESS_TOKEN_URL = "https://idp.example.com/oauth/token"

    def get_user_details(self, response):
        return {"username": response["login"], "email": response["email"]}


def begin(request, backend_name):
    strategy = load_strategy(request)
    backend = load_backend(strategy, backend_name, redirect_uri="/complete/")
    return do_auth(backend, redirect_name="next")


def complete(request, backend_name):
    strategy = load_strategy(request)
    backend = load_backend(strategy, backend_name, redirect_uri="/complete/")
    return do_complete(backend, login=lambda b, user, social: login(request, user), user=request.user)


@psa("social:complete")
def exchange_token(request, backend):
    user = backend.do_auth(request.GET.get("access_token"))
    if user is None:
        return JsonResponse({"error": "auth failed"}, status=401)
    login(request, user)
    return JsonResponse({"username": user.username})


def finish_oauth(backend: BaseOAuth2):
    return backend.auth_complete()
