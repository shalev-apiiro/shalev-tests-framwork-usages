# Python.Pydantic.json -> "Pydantic Python" [InputValidation]
# Expected: import pydantic; methods model_validate_json, model_validate, validate_python
from datetime import datetime
from typing import Literal

from flask import Flask, abort, request
from pydantic import BaseModel, TypeAdapter, ValidationError

app = Flask(__name__)


class PaymentEvent(BaseModel):
    id: str
    type: Literal["payment.succeeded", "payment.failed", "payment.refunded"]
    amount_cents: int
    currency: str
    created_at: datetime


class RefundLine(BaseModel):
    order_id: int
    amount_cents: int


refund_lines = TypeAdapter(list[RefundLine])


@app.post("/webhooks/payments")
def payment_webhook():
    try:
        event = PaymentEvent.model_validate_json(request.get_data())
    except ValidationError:
        abort(400)
    app.logger.info("payment event %s (%s)", event.id, event.type)
    return {"received": True}


@app.post("/refunds/batch")
def refund_batch():
    try:
        lines = refund_lines.validate_python(request.get_json(force=True))
    except ValidationError as exc:
        return {"errors": exc.errors(include_input=False)}, 422
    return {"queued": len(lines)}


def load_cached_event(raw: dict) -> PaymentEvent:
    return PaymentEvent.model_validate(raw)
