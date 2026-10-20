# Python.Pysaml2.json -> "PySAML2 Python" [SSO]
# Expected: import saml2; methods prepare_for_authenticate + parse_authn_request_response
from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT
from saml2.client import Saml2Client
from saml2.config import SPConfig

SP_SETTINGS = {
    "entityid": "https://sp.example.com/metadata",
    "service": {
        "sp": {
            "endpoints": {"assertion_consumer_service": [("https://sp.example.com/acs", BINDING_HTTP_POST)]},
        }
    },
    "metadata": {"remote": [{"url": "https://idp.example.com/metadata"}]},
}


def build_client() -> Saml2Client:
    config = SPConfig()
    config.load(SP_SETTINGS)
    return Saml2Client(config=config)


def start_login(client: Saml2Client):
    request_id, info = client.prepare_for_authenticate(
        entityid="https://idp.example.com/metadata", binding=BINDING_HTTP_REDIRECT
    )
    redirect_url = dict(info["headers"])["Location"]
    return request_id, redirect_url


def finish_login(client: Saml2Client, saml_response: str, outstanding: dict):
    authn_response = client.parse_authn_request_response(saml_response, BINDING_HTTP_POST, outstanding)
    return authn_response.get_identity(), authn_response.name_id
