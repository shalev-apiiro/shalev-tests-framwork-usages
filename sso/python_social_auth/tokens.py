# Python.PythonSocialAuth.json -> "Python Social Auth Python" [SSO]
# Expected: import social_django; method load_strategy
# Nightly job that refreshes provider access tokens before calling the provider's API for each user.
import logging

import requests
from social_core.exceptions import AuthException
from social_django.models import UserSocialAuth
from social_django.utils import load_strategy

log = logging.getLogger(__name__)


def refresh_provider_tokens(provider: str = "acme-id") -> int:
    strategy = load_strategy()
    refreshed = 0
    for social in UserSocialAuth.objects.filter(provider=provider).select_related("user"):
        if not social.access_token_expired():
            continue
        try:
            social.refresh_token(strategy)
        except (AuthException, requests.RequestException):
            log.warning("could not refresh %s token for user %s", provider, social.user_id)
            continue
        refreshed += 1
    return refreshed
