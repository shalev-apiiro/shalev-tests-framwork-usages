# Python.DjangoAllauthSSO.json -> "Django Allauth SSO Python" [SSO]
# Expected: import allauth.socialaccount; method pre_social_login
# Registered with SOCIALACCOUNT_ADAPTER = "accounts.adapter.CompanySocialAccountAdapter".
from allauth.account.models import EmailAddress
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect


class CompanySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin: SocialLogin):
        super().pre_social_login(request, sociallogin)

        email = (sociallogin.user.email or "").lower()
        if email.rpartition("@")[2] not in settings.SSO_ALLOWED_DOMAINS:
            messages.error(request, "Sign in with your company account.")
            raise ImmediateHttpResponse(redirect("account_login"))

        if sociallogin.is_existing:
            return
        existing = EmailAddress.objects.filter(email__iexact=email, verified=True).select_related("user").first()
        if existing is not None:
            sociallogin.connect(request, existing.user)

    def is_auto_signup_allowed(self, request, sociallogin: SocialLogin) -> bool:
        return True
