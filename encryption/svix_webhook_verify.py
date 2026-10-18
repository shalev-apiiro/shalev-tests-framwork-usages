# Python.Svix.json -> "Svix Python" [Encryption]
# Expected: import svix.webhooks, method verify
import os

from svix.webhooks import Webhook, WebhookVerificationError


def handle_webhook(payload: bytes, headers: dict) -> dict:
    wh = Webhook(os.environ["SVIX_WEBHOOK_SECRET"])
    try:
        return wh.verify(payload, headers)
    except WebhookVerificationError:
        raise PermissionError("invalid webhook signature")
