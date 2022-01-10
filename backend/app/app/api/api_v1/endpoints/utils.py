from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.utilities import send_web_contact_email
from app.schemas import EmailContent

router = APIRouter()


@router.post("/contact-us", response_model=schemas.Msg, status_code=201)
def send_email(*, data: EmailContent) -> Any:
    """
    Standard app contact us.
    """
    send_web_contact_email(data=data)
    return {"msg": "Web contact email sent"}

