from __future__ import annotations
from typing import Optional
from pydantic import Field, EmailStr
from uuid import UUID
from datetime import datetime

from app.schema_types import InvitationResponseType
from .base_schema import BaseSchema


class TeamInInvitation(BaseSchema):
    id: Optional[UUID] = None
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class InvitationBase(BaseSchema):
    full_name: Optional[str] = Field(None, description="Name of invited team member.")
    email: Optional[EmailStr] = Field(None, description="Email of invited team member.")
    sender_id: Optional[UUID] = Field(None, description="Team custodian responsible for the invitation.")
    team_id: Optional[UUID] = Field(None, description="Invitation team identity.")


class InvitationCreate(InvitationBase):
    full_name: str = Field(None, description="Name of invited team member.")
    email: EmailStr = Field(None, description="Email of invited team member.")
    response: InvitationResponseType = Field(
        default=InvitationResponseType.WAITING, description="Invitee current response."
    )


class InvitationUpdate(InvitationBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the invitation.")
    response: InvitationResponseType = Field(..., description="Invitee current response.")


class InvitationInDBBase(InvitationBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the invitation.")
    sender_id: UUID = Field(..., description="Team custodian responsible for the invitation.")
    team_id: UUID = Field(..., description="Invitation team identity.")
    team: TeamInInvitation = Field(..., description="Invitation team details.")
    created: datetime = Field(..., description="Automatically generated datetime of creation.")
    response: InvitationResponseType = Field(
        default=InvitationResponseType.WAITING, description="Invitee current response."
    )

    class Config:
        orm_mode = True


# Properties to return to client
class Invitation(InvitationInDBBase):
    pass


# Properties properties stored in DB
class InvitationInDB(InvitationInDBBase):
    pass
