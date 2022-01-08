from __future__ import annotations
from typing import Optional, Union, Dict, Any, List, TYPE_CHECKING
from pydantic import BaseModel, Field, AnyHttpUrl, validator
from uuid import UUID
from datetime import date, datetime
import json
from neomodel.relationship_manager import ZeroOrMore
from neomodel import One

from chapisha import WorkMetadata as ChapishaWorkMetadata

from app.schema_types import MimeType
from app.schema_types import WorkStateType
from app.schemas.subject import Subject
from app.schemas.creator import CreatorSummary
from app.schemas.contributor import ContributorSummary
from .base_schema import BaseSchema, MetadataBaseCreate
from app.schema_types import BaseEnum

if TYPE_CHECKING:
    from app.schemas import (
        ContributorCreate,
        Contributor,
        HistoryCreate,
        History,
        Subject,
        Contract,
        CreatorSummary,
        CreatorMini,
        ContributorSummary,
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


class BaseSource(BaseModel):
    data: str
    name: str


class WorkMetadataCreate(MetadataBaseCreate):
    uid: Optional[str] = Field(
        ..., description="UUID, DOI or ISBN of the creative work. A UUID will be generated if not included."
    )
    isodate: Optional[date] = Field(
        None, alias="date", description="The publication date of the creative work. Provide in ISO format, YYYY-MM-DD."
    )
    language: Optional[str] = Field(
        None,
        description="Specify the language of the creative work. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    long_rights: Optional[List[str]] = Field(
        None,
        alias="long-rights",
        description="Information about copyright held in and over the creative work. Formatted as you wish it to appear.",
    )
    publisher: Optional[str] = Field(
        None, description="Name of a person, organisation, etc.  responsible for making the creative work available.",
    )
    publisher_uri: Optional[AnyHttpUrl] = Field(
        None, alias="publisher-uri", description="The URI for the creative work.",
    )
    work_uri: Optional[AnyHttpUrl] = Field(
        None, alias="work-uri", description="The URI for the publisher of the creative work.",
    )
    word_count: Optional[int] = Field(
        None, alias="word-count", description="Total word count of the creative work.",
    )

    class Config:
        allow_population_by_field_name = True


class WorkMetadataUpdate(WorkMetadataCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class WorkMetadataInDBBase(WorkMetadataCreate):
    # Identifier managed programmatically
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    subject: List[Subject] = Field([], description="A list of topics of the resource.")
    creator: List[CreatorSummary] = Field([], description="List of summary creator profiles.")
    contributor: Optional[List[ContributorSummary]] = Field([], description="Contributors to the creative work.")
    isActive: bool = Field(..., description="Whether the work is publically accessible.")
    isPrivate: bool = Field(..., description="Whether the work is private to creators with appropriate authorisation.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True

    @validator("subject", pre=True)
    def evaluate_subject(cls, v):
        if isinstance(v, ZeroOrMore):
            return [Subject.from_orm(s) for s in v.all()]
        return v

    @validator("creator", pre=True)
    def evaluate_creator(cls, v):
        if isinstance(v, ZeroOrMore):
            return [CreatorSummary.from_orm(c) for c in v.all()]
        return v

    @validator("contributor", pre=True)
    def evaluate_contributor(cls, v):
        if isinstance(v, ZeroOrMore):
            return [ContributorSummary.from_orm(c) for c in v.all()]
        return v


class WorkMetadata(WorkMetadataInDBBase):
    pass


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

    @validator("metadata", pre=True)
    def evaluate_metadata(cls, v):
        if isinstance(v, One):
            return WorkMetadataInDBBase.from_orm(v.single())
        return v


class Work(WorkInDB):
    # history: List[History] = Field(..., description="State history definitions.")
    contract: Optional[Contract] = Field(None, description="Contract between contributors to this creative work.")

    class Config:
        orm_mode = True

    @validator("contract", pre=True)
    def evaluate_contract(cls, v):
        if isinstance(v, One):
            return Contract.from_orm(v.single())
        return v


########################################################################################################################
# SPECIAL PURPOSE SCHEMAS
########################################################################################################################


class WorkMetadataLineSummary(BaseSchema):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    uid: Optional[str] = Field(
        ..., description="UUID, DOI or ISBN of the creative work. A UUID will be generated if not included."
    )
    creator: List[CreatorMini] = Field([], description="List of summary creator profiles.")
    title: Optional[str] = Field(None, description="A human-readable name given to the resource.")
    description: Optional[str] = Field(
        None, description="A short, single-sentence summary of the creative work.",
    )
    long_description: Optional[str] = Field(
        None, description="The pitch, or jacket-cover, description of the creative work.",
    )
    subject: List[Subject] = Field([], description="A list of topics of the resource.")
    isodate: Optional[date] = Field(
        None, description="The publication date of the creative work. Provide in ISO format, YYYY-MM-DD."
    )
    word_count: Optional[int] = Field(
        None, description="Total word count of the creative work.",
    )

    class Config:
        orm_mode = True

    @validator("subject", pre=True)
    def evaluate_subject(cls, v):
        if isinstance(v, ZeroOrMore):
            return [Subject.from_orm(s) for s in v.all()]
        return v

    @validator("creator", pre=True)
    def evaluate_creator(cls, v):
        if isinstance(v, ZeroOrMore):
            return [CreatorMini.from_orm(c) for c in v.all()]
        return v


class WorkMetadataSummary(WorkMetadataLineSummary):
    uid: Optional[str] = Field(
        ..., description="UUID, DOI or ISBN of the creative work. A UUID will be generated if not included."
    )
    creator: List[CreatorSummary] = Field([], description="List of summary creator profiles.")
    contributor: Optional[List[ContributorSummary]] = Field([], description="Contributors to the creative work.")
    language: Optional[str] = Field(
        None,
        description="Specify the language of the creative work. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
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
    rights: Optional[str] = Field(
        None, description="Information about rights held in and over the resource.",
    )

    class Config:
        orm_mode = True

    @validator("creator", pre=True)
    def evaluate_creator(cls, v):
        if isinstance(v, ZeroOrMore):
            return [CreatorSummary.from_orm(c) for c in v.all()]
        return v

    @validator("contributor", pre=True)
    def evaluate_contributor(cls, v):
        if isinstance(v, ZeroOrMore):
            return [ContributorSummary.from_orm(c) for c in v.all()]
        return v


class WorkLineSummary(BaseSchema):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    state: WorkStateType = Field(..., description="The current work state.")
    metadata: WorkMetadataLineSummary = Field(..., description="Subset of metadata from work.")
    spine: Optional[List[str]] = Field(
        [], description="Spine list of contents for the creative work.",
    )
    first500: Optional[str] = Field(None, description="First 500 words (approx.) of first chapter of creative work.")
    created: date = Field(..., description="Automatically generated date work was created.")

    class Config:
        orm_mode = True

    @validator("metadata", pre=True)
    def evaluate_metadata(cls, v):
        if isinstance(v, One):
            return WorkMetadataLineSummary.from_orm(v.single())
        return v


class WorkSummary(WorkLineSummary):
    dedication: Optional[list[str]] = Field(None)
    price: Optional[int] = Field(
        None, description="Maximum price to be charged for reading. In US$ cents.",
    )
    start_page: Optional[int] = Field(
        default=0, description="Starting chapter for stream.",
    )
    metadata: WorkMetadataSummary = Field(..., description="Subset of metadata from work.")

    class Config:
        orm_mode = True

    @validator("metadata", pre=True)
    def evaluate_metadata(cls, v):
        if isinstance(v, One):
            return WorkMetadataSummary.from_orm(v.single())
        return v


from app.schemas.contributor import Contributor
from app.schemas.subject import Subject
from app.schemas.creator import CreatorSummary, CreatorMini
from app.schemas.history import History
from app.schemas.contract import Contract

WorkMetadataCreate.update_forward_refs()
WorkMetadataInDBBase.update_forward_refs()
WorkMetadataLineSummary.update_forward_refs()
WorkMetadata.update_forward_refs()
WorkMetadataSummary.update_forward_refs()
WorkSummary.update_forward_refs()
WorkInDB.update_forward_refs()
Work.update_forward_refs()
