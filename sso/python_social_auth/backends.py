# Python.PythonSocialAuth.json -> "Python Social Auth Python" [SSO]
# Expected: import social_core; method auth_complete
# Listed in AUTHENTICATION_BACKENDS as "accounts.social.backends.AcmeIdOAuth2".
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import AuthPolicyError


class AcmeIdOAuth2(BaseOAuth2):
    name = "acme-id"
    AUTHORIZATION_URL = "https://id.acme.example/oauth2/authorize"
    ACCESS_TOKEN_URL = "https://id.acme.example/oauth2/token"
    ACCESS_TOKEN_METHOD = "POST"
    REVOKE_TOKEN_URL = "https://id.acme.example/oauth2/revoke"
    DEFAULT_SCOPE = ["openid", "profile", "email", "groups"]
    REDIRECT_STATE = False
    EXTRA_DATA = [("refresh_token", "refresh_token", True), ("expires_in", "expires")]

    def auth_complete(self, *args, **kwargs):
        tenant = self.data.get("tenant")
        if tenant and tenant != self.setting("TENANT"):
            raise AuthPolicyError(self, f"tenant {tenant} is not allowed", stage="callback")
        return super().auth_complete(*args, **kwargs)

    def get_user_details(self, response):
        return {
            "username": response["preferred_username"],
            "email": response["email"],
            "first_name": response.get("given_name", ""),
            "last_name": response.get("family_name", ""),
        }

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json(
            "https://id.acme.example/oauth2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
