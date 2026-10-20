# Python.Djangosaml2.json -> "Django SAML2 Python" [SSO]
# Expected: import djangosaml2; methods get_saml_user + post_login_hook
from djangosaml2.backends import Saml2Backend
from djangosaml2.views import AssertionConsumerServiceView


class CompanySaml2Backend(Saml2Backend):
    def get_saml_user(self, request, session_info):
        user = super().get_saml_user(request, session_info)
        if user is not None and not user.email.endswith("@example.com"):
            return None
        return user


class CompanyAcsView(AssertionConsumerServiceView):
    def post_login_hook(self, request, user, session_info):
        request.session["saml_name_id"] = str(session_info["name_id"])
        super().post_login_hook(request, user, session_info)
