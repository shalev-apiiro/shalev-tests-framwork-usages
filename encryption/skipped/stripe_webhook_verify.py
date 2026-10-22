# NEGATIVE SAMPLE: Stripe webhook verification (row 61) was deliberately skipped in apiiro/lim PR #53633,
# so this file must NOT be detected as an Encryption control.
# Expected: nothing (Stripe Python only matches Payments `create` calls)
import os

import stripe

ENDPOINT_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]


def handle_webhook(payload: bytes, sig_header: str):
    try:
        return stripe.Webhook.construct_event(payload, sig_header, ENDPOINT_SECRET)
    except stripe.SignatureVerificationError:
        raise PermissionError("invalid stripe signature")


def check_signature_only(payload: str, sig_header: str) -> bool:
    return stripe.WebhookSignature.verify_header(payload, sig_header, ENDPOINT_SECRET)
