from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import stripe

from app import crud, models, schemas, schema_types
from app.api import deps
from app.core.config import settings


router = APIRouter()
stripe.api_key = settings.STRIPE_API_KEY


def calculate_order_amount(amount: int) -> int:
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return amount


@router.post("/", response_model=schemas.StripeIntentResponse)
def create_payment(*, payment: schemas.StripePaymentIntent) -> Any:
    try:
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(payment.amount), currency=payment.currency.value
        )
        return {"clientSecret": intent["client_secret"]}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

