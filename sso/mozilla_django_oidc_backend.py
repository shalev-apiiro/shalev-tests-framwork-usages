# Python.MozillaDjangoOidc.json -> "Mozilla Django OIDC Python" [SSO]
# Expected: import mozilla_django_oidc; methods verify_claims + filter_users_by_claims
# Configured with AUTHENTICATION_BACKENDS = ["accounts.oidc.CompanyOIDCBackend"].
from django.conf import settings
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CompanyOIDCBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        if not super().verify_claims(claims):
            return False
        if not claims.get("email_verified", False):
            return False
        return claims["email"].lower().endswith(f"@{settings.OIDC_ALLOWED_EMAIL_DOMAIN}")

    def filter_users_by_claims(self, claims):
        subject = claims.get("sub")
        if subject:
            users = self.UserModel.objects.filter(profile__oidc_subject=subject)
            if users.exists():
                return users
        return super().filter_users_by_claims(claims)

    def create_user(self, claims):
        user = super().create_user(claims)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save(update_fields=["first_name", "last_name"])
        user.profile.oidc_subject = claims["sub"]
        user.profile.save(update_fields=["oidc_subject"])
        return user

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", user.first_name)
        user.last_name = claims.get("family_name", user.last_name)
        user.save(update_fields=["first_name", "last_name"])
        return user
