# Python.DjangoAllauth.json -> "Django Allauth Python" [Authentication]
# Expected: imports allauth.account / allauth.headless.contrib.rest_framework.authentication /
#           allauth.headless.contrib.ninja.security; decorators verified_email_required +
#           reauthentication_required; method raise_if_reauthentication_required
from allauth.account.decorators import reauthentication_required, verified_email_required
from allauth.account.reauthentication import raise_if_reauthentication_required
from allauth.headless.contrib.ninja.security import x_session_token_auth
from allauth.headless.contrib.rest_framework.authentication import XSessionTokenAuthentication
from django.http import HttpResponse
from ninja import NinjaAPI
from rest_framework.views import APIView


@verified_email_required
def dashboard(request):
    return HttpResponse("verified users only")


@reauthentication_required
def change_email(request):
    return HttpResponse("recently re-authenticated users only")


def rotate_api_token(request):
    raise_if_reauthentication_required(request)
    return HttpResponse("token rotated")


class AccountView(APIView):
    authentication_classes = [XSessionTokenAuthentication]

    def get(self, request):
        return HttpResponse(request.user.email)


api = NinjaAPI(auth=x_session_token_auth)


@api.get("/me")
def me(request):
    return {"email": request.user.email}
