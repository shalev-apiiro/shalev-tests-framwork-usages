# Python.Slack.json (extended) -> "Slack SDK Python" [Messaging, Encryption]
# Expected: import slack_sdk.signature, methods is_valid_request / is_valid
import os

from slack_sdk.signature import SignatureVerifier

verifier = SignatureVerifier(signing_secret=os.environ["SLACK_SIGNING_SECRET"])


def is_slack_request(body: str, headers: dict) -> bool:
    return verifier.is_valid_request(body, headers)


def is_slack_request_parts(body: str, timestamp: str, signature: str) -> bool:
    return verifier.is_valid(body, timestamp, signature)
