from __future__ import annotations
from typing import Optional, Dict, Any, List
from pydantic import Field, validator
from uuid import UUID
from datetime import date

from .base_schema import BaseSchema


class SubjectCreate(BaseSchema):
    term: str = Field(..., description="A descriptive term.")


class SubjectUpdate(SubjectCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")

    class Config:
        orm_mode = True


class SubjectInDB(SubjectCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class Subject(SubjectInDB):
    pass
