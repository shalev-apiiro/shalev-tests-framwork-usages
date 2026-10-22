# NEGATIVE SAMPLE: Svix webhook verification (row 62) was deliberately skipped in apiiro/lim PR #53633,
# so this file must NOT be detected as an Encryption control.
# Expected: no framework usage detected
import os

from svix.webhooks import Webhook, WebhookVerificationError


def handle_webhook(payload: bytes, headers: dict) -> dict:
    wh = Webhook(os.environ["SVIX_WEBHOOK_SECRET"])
    try:
        return wh.verify(payload, headers)
    except WebhookVerificationError:
        raise PermissionError("invalid webhook signature")
