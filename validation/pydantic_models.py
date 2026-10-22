# Python.Pydantic.json -> "Pydantic Python" [InputValidation]
# Expected: import pydantic; decorators field_validator, model_validator, validate_call
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, validate_call


class Address(BaseModel):
    line1: str = Field(min_length=1, max_length=120)
    city: str = Field(min_length=1, max_length=80)
    country: str = Field(pattern=r"^[A-Z]{2}$")
    postal_code: str = Field(min_length=3, max_length=10)


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    confirm_password: str
    birth_date: date
    address: Address

    @field_validator("password")
    @classmethod
    def password_has_mixed_characters(cls, value: str) -> str:
        if value.isalpha() or value.isdigit():
            raise ValueError("password must mix letters and digits")
        return value

    @model_validator(mode="after")
    def passwords_match(self) -> "SignupRequest":
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self


@validate_call
def apply_discount(price: Decimal, percent: int = Field(ge=0, le=90)) -> Decimal:
    return (price * (100 - percent) / 100).quantize(Decimal("0.01"))
