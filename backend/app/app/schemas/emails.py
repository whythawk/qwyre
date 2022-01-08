from pydantic import BaseModel, EmailStr
from typing import List


class EmailContent(BaseModel):
    email: EmailStr
    subject: str
    content: str


class EmailValidation(BaseModel):
    email: EmailStr
    subject: str
    token: str


class ConfirmExpressionOfInterest(BaseModel):
    email: EmailStr
    subject: str
    contract_link: str
    workspace_link: str
    work_title: str


class ReceiveExpressionOfInterest(BaseModel):
    emails: List[EmailStr]
    subject: str
    creator_link: str
    creator: str
    creator_email: EmailStr
    contract_link: str
    workspace_link: str
    work_title: str
