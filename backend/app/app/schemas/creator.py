from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from pydantic import Field, AnyHttpUrl, AnyUrl, validator
from uuid import UUID
from datetime import date
from neomodel.relationship_manager import ZeroOrMore

from .base_schema import BaseSchema, MetadataBaseCreate

if TYPE_CHECKING:
    from app.schemas import Subject  # noqa: F401


class CreatorCreate(MetadataBaseCreate):
    creator: Optional[str] = Field(None, description="The public name a creator wishes to be called.")
    wallet: Optional[str] = Field(None, description="Payment pointer for web monetization.")
    website: Optional[AnyHttpUrl] = Field(None, description="Payment pointer for web monetization.")


class CreatorUpdate(CreatorCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class CreatorInDB(CreatorCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    subject: List[Subject] = Field([], description="A list of topics of the resource.")
    isActive: bool = Field(..., description="Whether the work is publically accessible.")
    isPrivate: bool = Field(..., description="Whether the work is private to creators with appropriate authorisation.")
    isBanned: bool = Field(..., description="Whether the creator has been banned by the moderators.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        use_enum_values = True
        orm_mode = True

    @validator("subject", pre=True)
    def evaluate_subjects(cls, v):
        if isinstance(v, ZeroOrMore):
            return [Subject.from_orm(c) for c in v.all()]
        return v


class Creator(CreatorInDB):
    pass


class CreatorSummary(BaseSchema):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    creator: Optional[str] = Field(None, description="The public name a creator wishes to be called.")
    description: Optional[str] = Field(
        None, description="A short, single-sentence summary of the creator.",
    )
    wallet: Optional[str] = Field(None, description="Payment pointer for web monetization.")
    website: Optional[AnyHttpUrl] = Field(None, description="Payment pointer for web monetization.")
    isActive: bool = Field(..., description="Whether the work is publically accessible.")
    isPrivate: bool = Field(..., description="Whether the work is private to creators with appropriate authorisation.")
    isBanned: bool = Field(..., description="Whether the creator has been banned by the moderators.")

    class Config:
        orm_mode = True


class CreatorProfile(BaseSchema):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    creator: Optional[str] = Field(None, description="The public name a creator wishes to be called.")
    description: Optional[str] = Field(
        None, description="A short, single-sentence summary of the creator.",
    )
    wallet: Optional[str] = Field(None, description="Payment pointer for web monetization.")
    website: Optional[AnyHttpUrl] = Field(None, description="Payment pointer for web monetization.")
    subject: List[Subject] = Field([], description="A list of topics of the resource.")

    class Config:
        orm_mode = True

    @validator("subject", pre=True)
    def evaluate_subjects(cls, v):
        if isinstance(v, ZeroOrMore):
            return [Subject.from_orm(c) for c in v.all()]
        return v


class CreatorMini(BaseSchema):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    creator: Optional[str] = Field(None, description="The public name a creator wishes to be called.")

    class Config:
        orm_mode = True


from app.schemas import Subject

CreatorInDB.update_forward_refs()
Creator.update_forward_refs()
CreatorProfile.update_forward_refs()
