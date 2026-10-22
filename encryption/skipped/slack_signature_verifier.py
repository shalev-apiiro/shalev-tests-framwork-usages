# NEGATIVE SAMPLE: Slack SDK signature verifier (row 55) was deliberately skipped in apiiro/lim PR #53633,
# so this file must NOT be detected as an Encryption control.
# Expected: Slack SDK Python [Messaging] only (import slack_sdk), never Encryption
import os

from slack_sdk.signature import SignatureVerifier

verifier = SignatureVerifier(signing_secret=os.environ["SLACK_SIGNING_SECRET"])


def is_slack_request(body: str, headers: dict) -> bool:
    return verifier.is_valid_request(body, headers)


def is_slack_request_parts(body: str, timestamp: str, signature: str) -> bool:
    return verifier.is_valid(body, timestamp, signature)
