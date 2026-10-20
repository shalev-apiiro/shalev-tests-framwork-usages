# Python.DjangoAllauthSSO.json -> "Django Allauth SSO Python" [SSO]
# Expected: import allauth.socialaccount; methods complete_social_login + pre_social_login
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter


class CompanySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin: SocialLogin):
        email = sociallogin.account.extra_data.get("email", "")
        if not email.endswith("@example.com"):
            raise PermissionError("only company accounts may sign in")
        return super().pre_social_login(request, sociallogin)


class CompanyOAuth2Adapter(OAuth2Adapter):
    provider_id = "company"
    access_token_url = "https://idp.example.com/oauth/token"
    authorize_url = "https://idp.example.com/oauth/authorize"
    profile_url = "https://idp.example.com/userinfo"

    def complete_login(self, request, app, token, **kwargs):
        profile = {"email": "alice@example.com"}
        login = self.get_provider().sociallogin_from_response(request, profile)
        return login


def finish_sso(request, sociallogin: SocialLogin):
    return complete_social_login(request, sociallogin)
