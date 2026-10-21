# Python.Djangosaml2.json -> "Django SAML2 Python" [SSO]
# Expected: import djangosaml2; method post_login_hook
# Wired in urls.py as path("saml2/acs/", CompanyAssertionConsumerServiceView.as_view(), name="saml2_acs").
import logging

from django.utils import timezone
from djangosaml2.views import AssertionConsumerServiceView

audit_log = logging.getLogger("audit.sso")


class CompanyAssertionConsumerServiceView(AssertionConsumerServiceView):
    def post_login_hook(self, request, user, session_info):
        super().post_login_hook(request, user, session_info)
        request.session["sso_idp"] = session_info["issuer"]
        request.session["sso_authenticated_at"] = timezone.now().isoformat()
        audit_log.info("SAML login user=%s idp=%s", user.pk, session_info["issuer"])
