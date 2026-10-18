# Python.Twilio.json (extended) -> "Twilio Python" [CustomerEngagementPlatform, Encryption]
# Expected: import twilio.request_validator, method validate
import os

from twilio.request_validator import RequestValidator

validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])


def is_twilio_request(url: str, params: dict, signature: str) -> bool:
    return validator.validate(url, params, signature)
