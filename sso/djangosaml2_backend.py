# Python.Djangosaml2.json -> "Django SAML2 Python" [SSO]
# Expected: import djangosaml2
# Configured with AUTHENTICATION_BACKENDS = ["accounts.saml.CompanySaml2Backend", ...].
from django.conf import settings
from django.contrib.auth.models import Group
from djangosaml2.backends import Saml2Backend


class CompanySaml2Backend(Saml2Backend):
    def is_authorized(self, attributes, attribute_mapping, idp_entityid, assertion_info, **kwargs) -> bool:
        if idp_entityid not in settings.SAML_TRUSTED_IDPS:
            return False
        groups = set(attributes.get("memberOf", []))
        return bool(groups & set(settings.SAML_ALLOWED_GROUPS))

    def clean_user_main_attribute(self, main_attribute):
        return main_attribute.strip().lower()

    def _update_user(self, user, attributes, attribute_mapping, force_save=False):
        user = super()._update_user(user, attributes, attribute_mapping, force_save=force_save)
        idp_groups = set(attributes.get("memberOf", []))
        user.is_staff = settings.SAML_STAFF_GROUP in idp_groups
        user.save(update_fields=["is_staff"])
        user.groups.set(Group.objects.filter(name__in=idp_groups))
        return user
