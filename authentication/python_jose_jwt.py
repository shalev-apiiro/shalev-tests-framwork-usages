# Python.PythonJose.json -> "Python Jose Python" [Authentication]
# Expected: methods jose.jwt.decode + jose.jws.verify
import json
import os
from functools import lru_cache

import requests
from jose import ExpiredSignatureError, JWTError, jws, jwt

ISSUER = os.environ["OIDC_ISSUER"]
AUDIENCE = os.environ["API_AUDIENCE"]
PARTNER_WEBHOOK_PUBLIC_KEY = os.environ["PARTNER_WEBHOOK_PUBLIC_KEY"]


class AuthenticationFailed(Exception):
    pass


@lru_cache(maxsize=1)
def _jwks() -> dict:
    response = requests.get(f"{ISSUER}/.well-known/jwks.json", timeout=5)
    response.raise_for_status()
    return response.json()


def authenticate_bearer(authorization_header: str) -> dict:
    scheme, _, token = authorization_header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise AuthenticationFailed("missing bearer token")
    try:
        return jwt.decode(token, _jwks(), algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
    except ExpiredSignatureError as exc:
        raise AuthenticationFailed("token expired") from exc
    except JWTError as exc:
        raise AuthenticationFailed("invalid token") from exc


def parse_partner_webhook(signed_body: str) -> dict:
    try:
        payload = jws.verify(signed_body, PARTNER_WEBHOOK_PUBLIC_KEY, algorithms=["ES256"])
    except JWTError as exc:
        raise AuthenticationFailed("webhook signature mismatch") from exc
    return json.loads(payload)
