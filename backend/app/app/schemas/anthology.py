from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from pydantic import Field
from uuid import UUID
from datetime import date

from app.schema_types import WorkStateType
from .base_schema import BaseSchema, MetadataBaseCreate

if TYPE_CHECKING:
    from app.schemas import (
        History,
        Subject,
        Contract,
        CreatorSummary,
        WorkSummary,
    )  # noqa: F401


class SeriesWorksCreate(BaseSchema):
    index: Optional[int] = Field(None, description="Order of the subscription (optional)")
    description: Optional[str] = Field(
        None, description="Optional notes as to why included in the series.",
    )


class SeriesWorksUpdate(SeriesWorksCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class SeriesWorksInDB(SeriesWorksCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    creator: Optional[str] = Field(None, description="The public name a creator wishes to be called.")
    work: UUID = Field(..., description="Reference UUID for a creative work.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class SeriesWorks(SeriesWorksInDB):
    pass


class SeriesCreate(MetadataBaseCreate):
    isodate: Optional[date] = Field(
        None, description="The publication date of the creative work. Provide in ISO format, YYYY-MM-DD."
    )
    state: WorkStateType = Field(..., description="The current work state.")


class SeriesUpdate(SeriesCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class SeriesInDB(SeriesCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    subject: List[Subject] = Field([], description="A list of topics of the resource.")
    works: Optional[List[WorkSummary]] = Field([], description="A list of included works.")
    curator: List[CreatorSummary] = Field([], description="List of summary creator profiles.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class Series(SeriesInDB):
    history: List[History] = Field(..., description="State history definitions.")
    contract: List[Contract] = Field(..., description="Contract between contributors to this series.")


class AnthologyCreate(MetadataBaseCreate):
    isodate: Optional[date] = Field(
        None, description="The publication date of the creative work. Provide in ISO format, YYYY-MM-DD."
    )
    state: WorkStateType = Field(..., description="The current work state.")


class AnthologyUpdate(AnthologyCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class AnthologyInDB(AnthologyCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    subject: List[Subject] = Field([], description="A list of topics of the resource.")
    works: Optional[List[WorkSummary]] = Field([], description="A list of included works.")
    series: Optional[List[SeriesWorks]] = Field([], description="A list of included series.")
    curator: List[CreatorSummary] = Field([], description="List of summary creator profiles.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class Anthology(AnthologyInDB):
    history: List[History] = Field(..., description="State history definitions.")
    contract: List[Contract] = Field(..., description="Contract between contributors to this series.")
