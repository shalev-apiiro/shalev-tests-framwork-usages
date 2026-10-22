# Python.Jsonschema.json -> "jsonschema Python" [InputValidation]
# Expected: import jsonschema; methods validate, is_valid
import json
from pathlib import Path

from flask import Flask, request
from jsonschema import Draft202012Validator, ValidationError, validate

app = Flask(__name__)

WEBHOOK_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["url", "events"],
    "additionalProperties": False,
    "properties": {
        "url": {"type": "string", "format": "uri", "pattern": "^https://"},
        "events": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"enum": ["push", "release", "issue"]}},
        "secret": {"type": "string", "minLength": 16},
    },
}

webhook_validator = Draft202012Validator(WEBHOOK_SCHEMA)


@app.post("/api/webhooks")
def create_webhook():
    payload = request.get_json(silent=True)
    if not webhook_validator.is_valid(payload):
        errors = [error.message for error in webhook_validator.iter_errors(payload)]
        return {"errors": errors}, 422
    return {"created": True}, 201


def load_pipeline_config(path: Path, schema_path: Path) -> dict:
    config = json.loads(path.read_text())
    schema = json.loads(schema_path.read_text())
    try:
        validate(instance=config, schema=schema)
    except ValidationError as exc:
        raise SystemExit(f"{path}: {exc.message}") from exc
    return config
