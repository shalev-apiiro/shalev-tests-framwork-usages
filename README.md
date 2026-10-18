# shalev-tests-framwork-usages

Python framework usage samples. One file per framework config.

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
