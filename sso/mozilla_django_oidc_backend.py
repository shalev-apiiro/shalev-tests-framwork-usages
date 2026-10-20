# Python.MozillaDjangoOidc.json -> "Mozilla Django OIDC Python" [SSO]
# Expected: import mozilla_django_oidc; methods verify_claims + filter_users_by_claims
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CompanyOIDCBackend(OIDCAuthenticationBackend):
    def verify_claims(self, claims):
        verified = super().verify_claims(claims)
        return verified and claims.get("email_verified", False)

    def filter_users_by_claims(self, claims):
        email = claims.get("email")
        if not email:
            return self.UserModel.objects.none()
        return super().filter_users_by_claims(claims)

    def create_user(self, claims):
        user = super().create_user(claims)
        user.first_name = claims.get("given_name", "")
        user.save()
        return user
