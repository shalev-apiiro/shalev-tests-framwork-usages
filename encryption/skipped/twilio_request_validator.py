# NEGATIVE SAMPLE: Twilio RequestValidator (row 64) was deliberately skipped in apiiro/lim PR #53633,
# so this file must NOT be detected as an Encryption control.
# Expected: nothing (Twilio Python only matches twilio.rest / twiml messaging calls)
import os

from twilio.request_validator import RequestValidator

validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])


def is_twilio_request(url: str, params: dict, signature: str) -> bool:
    return validator.validate(url, params, signature)
