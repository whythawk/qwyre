from __future__ import annotations
from typing import Optional, Dict, Any, List, TYPE_CHECKING
from pydantic import BaseModel, Field, AnyHttpUrl, validator
from uuid import UUID
from datetime import date

from chapisha import WorkMetadata as ChapishaWorkMetadata

from app.schema_types import MimeType
from app.schema_types import WorkStateType
from .base_schema import BaseSchema, MetadataBaseCreate

if TYPE_CHECKING:
    from app.schemas import (
        ContributorCreate,
        Contributor,
        HistoryCreate,
        History,
        Subject,
        Contract,
        CreatorSummary,
    )  # noqa: F401


class BuildData(BaseModel):
    metadata: ChapishaWorkMetadata = Field(...)
    cover: str = Field(...)
    text: str = Field(...)
    dedication: Optional[list[str]] = Field(None)
    work: Optional[str] = Field(None)


class DataSource(BaseModel):
    mime: MimeType
    data: bytes
    name: Optional[str]


class WorkMetadataCreate(MetadataBaseCreate):
    uid: Optional[str] = Field(
        ..., description="UUID, DOI or ISBN of the creative work. A UUID will be generated if not included."
    )
    isodate: Optional[date] = Field(
        None, description="The publication date of the creative work. Provide in ISO format, YYYY-MM-DD."
    )
    language: Optional[str] = Field(
        None,
        description="Specify the language of the creative work. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    long_rights: Optional[List[str]] = Field(
        None,
        description="Information about copyright held in and over the creative work. Formatted as you wish it to appear.",
    )
    publisher: Optional[str] = Field(
        None, description="Name of a person, organisation, etc.  responsible for making the creative work available.",
    )
    publisher_uri: Optional[AnyHttpUrl] = Field(
        None, description="The URI for the creative work.",
    )
    work_uri: Optional[AnyHttpUrl] = Field(
        None, description="The URI for the publisher of the creative work.",
    )
    word_count: Optional[int] = Field(
        None, description="Total word count of the creative work.",
    )


class WorkMetadataUpdate(WorkMetadataCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")

    class Config:
        orm_mode = True


class WorkMetadataInDBBase(WorkMetadataCreate):
    # Identifier managed programmatically
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    subject: List[Subject] = Field([], description="A list of topics of the resource.")
    creator: List[CreatorSummary] = Field([], description="List of summary creator profiles.")
    contributor: Optional[List[Contributor]] = Field([], description="Contributors to the creative work.")
    isActive: bool = Field(..., description="Whether the work is publically accessible.")
    isPrivate: bool = Field(..., description="Whether the work is private to creators with appropriate authorisation.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class WorkMetadata(WorkMetadataInDBBase):
    pass


class WorkSummary(BaseSchema):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    title: Optional[str] = Field(None, description="A human-readable name given to the resource.")
    description: Optional[str] = Field(
        None, description="A short, single-sentence summary of the creative work.",
    )
    creator: List[CreatorSummary] = Field([], description="List of summary creator profiles.")
    subject: List[Subject] = Field([], description="A list of topics of the resource.")
    isodate: Optional[date] = Field(
        None, description="The publication date of the creative work. Provide in ISO format, YYYY-MM-DD."
    )
    language: Optional[str] = Field(
        None,
        description="Specify the language of the creative work. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    word_count: Optional[int] = Field(
        None, description="Total word count of the creative work.",
    )

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class WorkCreate(BaseSchema):
    dedication: Optional[list[str]] = Field(None)
    price: Optional[int] = Field(
        None, description="Maximum price to be charged for reading. In US$ cents.",
    )
    stream: Optional[List[List[str]]] = Field(
        [],
        description="Creative work structured for streaming. Structured as list of pages, containing lists of tags and words.",
    )
    spine: Optional[List[str]] = Field(
        [], description="Spine list of contents for the creative work.",
    )
    first500: Optional[str] = Field(None, description="First 500 words (approx.) of first chapter of creative work.")
    start_page: Optional[int] = Field(
        default=0, description="Starting chapter for stream.",
    )
    state: WorkStateType = Field(..., description="The current work state.")


class WorkUpdate(WorkCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")

    class Config:
        orm_mode = True


class WorkInDB(WorkCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    metadata: WorkMetadataInDBBase = Field(..., description="Subset of metadata from work.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class Work(WorkInDB):
    history: List[History] = Field(..., description="State history definitions.")
    contract: List[Contract] = Field(..., description="Contract between contributors to this creative work.")


from app.schemas.contributor import Contributor
from app.schemas.subject import Subject
from app.schemas.creator import CreatorSummary
from app.schemas.history import History
from app.schemas.contract import Contract

WorkMetadataCreate.update_forward_refs()
WorkMetadataInDBBase.update_forward_refs()
WorkMetadata.update_forward_refs()
WorkSummary.update_forward_refs()
WorkInDB.update_forward_refs()
Work.update_forward_refs()
