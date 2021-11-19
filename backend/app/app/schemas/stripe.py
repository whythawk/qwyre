from pydantic import BaseModel, validator

from app.schema_types import CurrencyType
from app.core.config import settings


class StripeIntentResponse(BaseModel):
    clientSecret: str


class StripePaymentIntent(BaseModel):
    currency: CurrencyType
    amount: int

    @validator("amount")
    def valid_amount(cls, v, values, **kwargs):
        if not isinstance(v, int):
            raise ValueError(f"Not a valid integer amount ({v}).")
        if v < settings.STRIPE_MINIMUM_CHARGE_AMOUNT:
            raise ValueError(f"Cannot accept a payment less than {values['currency'].describe()} {v/100:.2f}.")
        return v
