# Python.Cerberus.json -> "Cerberus Python" [InputValidation]
# Expected: import cerberus; methods validate, validated
import csv
from pathlib import Path

from cerberus import Validator

CUSTOMER_ROW_SCHEMA = {
    "customer_id": {"type": "integer", "coerce": int, "min": 1, "required": True},
    "email": {"type": "string", "regex": r"^[^@\s]+@[^@\s]+\.[^@\s]+$", "required": True},
    "plan": {"type": "string", "allowed": ["free", "team", "enterprise"], "required": True},
    "seats": {"type": "integer", "coerce": int, "min": 1, "max": 10000, "default": 1},
}

row_validator = Validator(CUSTOMER_ROW_SCHEMA, purge_unknown=True)


def import_customers(csv_path: Path) -> tuple[list[dict], list[tuple[int, dict]]]:
    accepted, rejected = [], []
    with csv_path.open(newline="") as handle:
        for line_number, row in enumerate(csv.DictReader(handle), start=2):
            if row_validator.validate(row):
                accepted.append(row_validator.document)
            else:
                rejected.append((line_number, row_validator.errors))
    return accepted, rejected


def normalize_settings(raw: dict) -> dict:
    schema = {"timezone": {"type": "string", "empty": False}, "digest_hour": {"type": "integer", "coerce": int, "min": 0, "max": 23}}
    settings = Validator(schema).validated(raw)
    if settings is None:
        raise ValueError("invalid settings")
    return settings
