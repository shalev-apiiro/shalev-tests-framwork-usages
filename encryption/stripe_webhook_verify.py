# Python.StripePayment.json (extended) -> "Stripe Python" [Encryption]
# Expected: import stripe, methods construct_event / verify_header
# (no `.create(` call in this file: the existing Payments `create` entry would win)
import os

import stripe

ENDPOINT_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]


def handle_webhook(payload: bytes, sig_header: str):
    try:
        return stripe.Webhook.construct_event(payload, sig_header, ENDPOINT_SECRET)
    except stripe.error.SignatureVerificationError:
        raise PermissionError("invalid stripe signature")


def check_signature_only(payload: str, sig_header: str) -> bool:
    return stripe.WebhookSignature.verify_header(payload, sig_header, ENDPOINT_SECRET)
