# shalev-tests-framwork-usages

Python framework usage samples. One file per framework config.

Security-control folders (`authentication/`, `authorization/`, `mfa/`, `sso/`, `kms/`) cover the configs added in apiiro/lim PR #53887.
No `requirements.txt` entries are added for them on purpose, so a match proves code-level detection, not dependency detection.
Each sample is written as code from a real application and was import-checked against the real libraries.
A library with several concerns gets a small package (one file per concern), shaped like the Django app or module a project would have.
"Should match" lists the config's own entries the file hits. Generic configs (Django, Flask, Starlette, logging, hashlib, requests and so on) can match too and are not listed.

## SessionManagement

| File | Config | Expected framework | Should match |
| --- | --- | --- | --- |
| `aiohttp_session_app.py` | `Python.AiohttpSession.json` | aiohttp-session Python | import `aiohttp_session`, `new_session`, `invalidate` |
| `django_sessions_views.py` | `Python.DjangoSessions.json` | Django Sessions Python | import `django.contrib.sessions...`, `cycle_key`, `acycle_key`, `logout`, `alogout` |
| `flask_builtin_session_app.py` | `Python.FlaskBuiltInSession.json` | Flask Session Python | `from flask import session` |
| `flask_session_app.py` | `Python.FlaskSession.json` | Flask-Session Python | import `flask_session`, `regenerate` |
| `flask_login_logout.py` | `Python.FlaskLoginSession.json` | Flask-Login Session Python | `logout_user` |
| `starlette_sessions_app.py` | `Python.StarletteSessionMiddleware.json` | Starlette Sessions Python | import `starlette.middleware.sessions` |

## Encryption (`encryption/`)

| File | Config | Expected framework | Should match |
| --- | --- | --- | --- |
| `argon2_password_hasher.py` | `Python.Argon2Cffi.json` | Argon2 Python | import `argon2` |
| `bcrypt_hashing.py` | `Python.Bcrypt.json` | Bcrypt Python | import `bcrypt` |
| `passlib_crypt_context.py` | `Python.Passlib.json` | Passlib Python | import `passlib.context`, `passlib.hash` |
| `aws_encryption_sdk_envelope.py` | `Python.AwsEncryptionSdk.json` | AWS Encryption SDK Python | import `aws_encryption_sdk` |
| `tink_aead.py` | `Python.Tink.json` | Google Tink Python | import `tink` |
| `sqlalchemy_utils_encrypted_columns.py` | `Python.SqlalchemyUtils.json` | SQLAlchemy-Utils Python | import `sqlalchemy_utils.StringEncryptedType`, `sqlalchemy_utils.types.encrypted...` |
| `svix_webhook_verify.py` | `Python.Svix.json` | Svix Python | import `svix.webhooks`, `verify` |
| `os_urandom_tokens.py` | `Python.OsUrandom.json` | os.urandom Python | import `os`, `urandom` |
| `random_system_random.py` | `Python.RandomSystemRandom.json` | random.SystemRandom Python | import `random`, `SystemRandom` |
| `secrets_tokens.py` | `Python.Secrets.json` | Secrets Python | import `secrets`, `token_bytes`, `token_hex`, `token_urlsafe`, `choice`, `randbelow`, `randbits`, `SystemRandom` |
| `werkzeug_password_hashing.py` | `Python.werkzeug.json` | Werkzeug Python (ApiServer + Encryption) | import `werkzeug.security.generate_password_hash` / `check_password_hash` |
| `pymongo_client_side_encryption.py` | `Python.pymongo.json` | MongoDB Python (DataStorage + Encryption) | import `pymongo.encryption`, `pymongo.encryption_options` |
| `slack_signature_verifier.py` | `Python.Slack.json` | Slack SDK Python (Messaging + Encryption) | import `slack_sdk.signature`, `is_valid_request`, `is_valid` |
| `stripe_webhook_verify.py` | `Python.StripePayment.json` | Stripe Python (Encryption) | import `stripe`, `construct_event`, `verify_header` |
| `twilio_request_validator.py` | `Python.Twilio.json` | Twilio Python (CustomerEngagementPlatform + Encryption) | import `twilio.request_validator`, `validate` |

## Authentication (`authentication/`)

| File | Config | Expected framework | Should match |
| --- | --- | --- | --- |
| `aiohttp_security_app.py` | `Python.AiohttpSecurity.json` | Aiohttp Security Python | `setup_security` (alias of `aiohttp_security.setup`), `check_authorized`; also aiohttp-session Python (`import aiohttp_session`) |
| `django_allauth/views.py` | `Python.DjangoAllauth.json` | Django Allauth Python | import `allauth.account`; decorators `verified_email_required`, `reauthentication_required` |
| `django_allauth/drf_api.py` | `Python.DjangoAllauth.json` | Django Allauth Python | import `allauth.headless.contrib.rest_framework.authentication` |
| `django_allauth/ninja_api.py` | `Python.DjangoAllauth.json` | Django Allauth Python | import `allauth.headless.contrib.ninja.security` |
| `flask_security_app.py` | `Python.FlaskSecurity.json` | Flask Security Python | import `flask_security`; decorators `auth_required`, `auth_token_required`, `http_auth_required`; `check_and_update_authn_fresh` |
| `python_jose_jwt.py` | `Python.PythonJose.json` | Python Jose Python | `jose.jwt.decode`, `jose.jws.verify` |
| `quart_auth_app.py` | `Python.QuartAuth.json` | Quart Auth Python | import `quart_auth`; decorators `login_required`, `basic_auth_required` |
| `starlette_authentication_app.py` | `Python.StarletteAuthentication.json` | Starlette Authentication Python | import `starlette.authentication`, `starlette.middleware.authentication`; decorator `requires`; `has_required_scope`, `Middleware` |

## Authorization (`authorization/`)

| File | Config | Expected framework | Should match |
| --- | --- | --- | --- |
| `aiohttp_security_permissions.py` | `Python.AiohttpSecurityAuthorization.json` | Aiohttp Security Authorization Python | `check_permission`, `permits` |
| `cerbos_check.py` | `Python.Cerbos.json` | Cerbos Python | `is_allowed`, `check_resources`, `plan_resources` |
| `django_graphql_jwt_schema.py` | `Python.DjangoGraphqlJwt.json` | Django Graphql JWT Python | decorators `permission_required`, `staff_member_required`, `superuser_required` |
| `django_rules/books/models.py` | `Python.DjangoRules.json` | Django Rules Python | import `rules.contrib.models` |
| `django_rules/books/admin.py` | `Python.DjangoRules.json` | Django Rules Python | import `rules.contrib.admin` |
| `django_rules/books/api.py` | `Python.DjangoRules.json` | Django Rules Python | import `rules.contrib.rest_framework` |
| `django_rules/books/views.py` | `Python.DjangoRules.json` | Django Rules Python | import `rules.contrib.views`; decorator `permission_required`; `rules.has_perm`, `rules.test_rule` |
| `django_rules/books/predicates.py` | `Python.DjangoRules.json` | — | nothing: predicate definitions only (`import rules` is not a config import) |
| `drf_api_key_permissions.py` | `Python.DjangorestframeworkApiKey.json` | Django REST Framework API Key Python | import `rest_framework_api_key`; `get_from_key` |
| `flask_security_roles.py` | `Python.FlaskSecurityAuthorization.json` | Flask Security Authorization Python | decorators `roles_required`, `roles_accepted`, `permissions_required`, `permissions_accepted`; `has_role`, `has_permission`; also Flask Security Python (`import flask_security`, `@auth_required`) |
| `strawberry_permissions_schema.py` | `Python.StrawberryPermissions.json` | Strawberry Permissions Python | import `strawberry.permission`, `strawberry.BasePermission`; `PermissionExtension` |
| `strawberry_django/catalog/schema.py` | `Python.StrawberryGraphqlDjangoPermissions.json` | Strawberry Django Permissions Python | import `strawberry_django.permissions`; `IsStaff` (in a resolver decorator). `HasPerm`, `HasSourcePerm`, `HasRetvalPerm`, `IsSuperuser` are used in class-body field assignments, which the matcher does not scan for calls |
| `strawberry_django/catalog/models.py` | `Python.StrawberryGraphqlDjangoPermissions.json` | — | nothing: the model the schema exposes |

## MultiFactorAuthentication (`mfa/`)

| File | Config | Expected framework | Should match |
| --- | --- | --- | --- |
| `cryptography_twofactor.py` | `Python.CryptographyMfa.json` | Cryptography MFA Python | import `cryptography.hazmat.primitives.twofactor`; `TOTP`, `HOTP`, `get_provisioning_uri` |
| `django_otp_views.py` | `Python.DjangoOtp.json` | Django OTP Python | import `django_otp`; `verify_token`, `match_token`, `random_token`; decorator `otp_required` |
| `passlib_totp.py` | `Python.PasslibMfa.json` | Passlib MFA Python | import `passlib.totp`; `to_uri` (the factory is built with `TOTP.using(...)`, so `TOTP` itself is not called) |
| `py_webauthn_ceremonies.py` | `Python.PyWebauthn.json` | Py WebAuthn Python | import `webauthn`; `generate_registration_options`, `verify_registration_response`, `generate_authentication_options`, `verify_authentication_response` |
| `pyotp_totp.py` | `Python.Pyotp.json` | PyOTP Python | import `pyotp`; `TOTP`, `HOTP`, `random_base32`, `provisioning_uri` |
| `python_fido2_server.py` | `Python.PythonFido2.json` | Python FIDO2 Python | import `fido2.server`; `register_begin`, `register_complete`, `authenticate_begin`, `authenticate_complete` |

## SSO (`sso/`)

| File | Config | Expected framework | Should match |
| --- | --- | --- | --- |
| `authlib_flask_oidc.py` | `Python.AuthlibSSO.json` | Authlib SSO Python | import `authlib.integrations.flask_client`; `authorize_redirect`, `authorize_access_token`, `parse_id_token` |
| `authlib_starlette_oidc.py` | `Python.AuthlibSSO.json` | Authlib SSO Python | import `authlib.integrations.starlette_client`; `authorize_redirect`, `authorize_access_token` |
| `django_allauth_social/adapter.py` | `Python.DjangoAllauthSSO.json` | Django Allauth SSO Python | import `allauth.socialaccount`; `pre_social_login` (the `super()` call); also Django Allauth Python (`import allauth.account`) |
| `django_allauth_social/views.py` | `Python.DjangoAllauthSSO.json` | Django Allauth SSO Python | import `allauth.socialaccount`; `complete_social_login` |
| `djangosaml2_backend.py` | `Python.Djangosaml2.json` | Django SAML2 Python | import `djangosaml2` |
| `djangosaml2_views.py` | `Python.Djangosaml2.json` | Django SAML2 Python | import `djangosaml2`; `post_login_hook` (the `super()` call) |
| `mozilla_django_oidc_backend.py` | `Python.MozillaDjangoOidc.json` | Mozilla Django OIDC Python | import `mozilla_django_oidc`; `verify_claims`, `filter_users_by_claims` (the `super()` calls) |
| `pysaml2_sp.py` | `Python.Pysaml2.json` | PySAML2 Python | import `saml2`; `prepare_for_authenticate`, `parse_authn_request_response` |
| `python3_saml_views.py` | `Python.Python3Saml.json` | Python3 SAML Python | import `onelogin.saml2`; `process_response`, `process_slo`, `get_sp_metadata` |
| `python_social_auth/backends.py` | `Python.PythonSocialAuth.json` | Python Social Auth Python | import `social_core`; `auth_complete` (the `super()` call) |
| `python_social_auth/views.py` | `Python.PythonSocialAuth.json` | Python Social Auth Python | import `social_core`, `social_django`; `do_auth`, `do_complete`; decorator `psa` |
| `python_social_auth/tokens.py` | `Python.PythonSocialAuth.json` | Python Social Auth Python | import `social_core`, `social_django`; `load_strategy` |

## KeyManagementService (`kms/`)

| File | Config | Expected framework | Should match |
| --- | --- | --- | --- |
| `cryptography_multifernet.py` | `Python.CryptographyKeyManagement.json` | Cryptography Key Management Python | `MultiFernet` |
| `pykcs11_hsm.py` | `Python.Pykcs11.json` | PyKCS11 Python | import `PyKCS11` |
| `python_pkcs11_hsm.py` | `Python.PythonPkcs11.json` | Python PKCS11 Python | import `pkcs11` |
| `yubihsm_keys.py` | `Python.PythonYubihsm.json` | Python YubiHSM Python | import `yubihsm` |
