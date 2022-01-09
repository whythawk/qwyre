from __future__ import annotations
from typing import Optional, Dict, Any
from pydantic import Field, validator
from uuid import UUID
from datetime import date

from .base_schema import BaseSchema


class SubscriptionCreate(BaseSchema):
    subscriber: UUID = Field(..., description="Reference UUID for a creator profile.")
    index: Optional[int] = Field(None, description="Order of the subscription (optional)")

    # @validator("anthology")
    # def evaluate_anthology(cls, v, values: Dict[str, Any]):
    #     if not values.get("series") and not values.get("creator") and not v:
    #         raise ValueError("Subscription must reference one of creator, series or anthology.")
    #     return v


class SubscriptionUpdate(SubscriptionCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class SubscriptionInDB(SubscriptionCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    creator: Optional[UUID] = Field(None, description="Reference UUID for a creator profile.")
    series: Optional[UUID] = Field(None, description="Reference UUID for a creative series.")
    anthology: Optional[UUID] = Field(None, description="Reference UUID for a creative anthology.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class Subscription(SubscriptionInDB):
    pass
