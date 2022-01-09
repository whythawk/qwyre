from __future__ import annotations
from typing import Optional, Dict, Any
from pydantic import Field, validator
from uuid import UUID
from datetime import date

from app.schema_types import WorkStateType
from .base_schema import BaseSchema


class HistoryCreate(BaseSchema):
    state: WorkStateType = Field(..., description="The work state.")
    expires: Optional[date] = Field(
        None, description="Expiry datetime for this state. Only valid for certain states, e.g. OFFERED."
    )
    description: Optional[str] = Field(
        None, description="Optional notes to the state change, including, e.g. text for an OFFER."
    )
    # work: Optional[UUID] = Field(None, description="Reference UUID to creative work.")
    # series: Optional[UUID] = Field(None, description="Reference UUID to a series.")
    # anthology: Optional[UUID] = Field(None, description="Reference UUID to an anthology.")

    # @validator("anthology")
    # def evaluate_creator(cls, v, values: Dict[str, Any]):
    #     if not values.get("series") and not values.get("work") and not v:
    #         raise ValueError("History must reference one of work, series or anthology.")
    #     return v


class HistoryUpdate(HistoryCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class HistoryInDB(HistoryCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    curator: UUID = Field(..., description="Reference UUID for a creator profile.")
    work: Optional[UUID] = Field(None, description="Reference UUID to creative work.")
    series: Optional[UUID] = Field(None, description="Reference UUID to a series.")
    anthology: Optional[UUID] = Field(None, description="Reference UUID to an anthology.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True

    @validator("anthology")
    def evaluate_creator(cls, v, values: Dict[str, Any]):
        if not values.get("series") and not values.get("work") and not v:
            raise ValueError("History must reference one of work, series or anthology.")
        return v


class History(HistoryInDB):
    pass

