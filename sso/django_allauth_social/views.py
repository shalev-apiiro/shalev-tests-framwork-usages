# Python.DjangoAllauthSSO.json -> "Django Allauth SSO Python" [SSO]
# Expected: import allauth.socialaccount; method complete_social_login
# Native mobile app sign-in: the app obtains a Google ID token itself and posts it here,
# the same way allauth's own Google One Tap view does.
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def mobile_google_login(request):
    id_token = request.POST.get("id_token")
    if not id_token:
        return JsonResponse({"error": "id_token is required"}, status=400)

    provider = get_adapter().get_provider(request, GoogleOAuth2Adapter.provider_id)
    try:
        sociallogin = provider.verify_token(request, {"id_token": id_token})
    except ValidationError:
        return JsonResponse({"error": "invalid id_token"}, status=401)

    complete_social_login(request, sociallogin)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "sign-in not completed"}, status=403)
    return JsonResponse({"user": request.user.get_username(), "session_key": request.session.session_key})
