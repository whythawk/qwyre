from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from pydantic import Field, validator
from uuid import UUID
from datetime import date
from neomodel.relationship_manager import ZeroOrMore
from neomodel import One

from app.schemas.subject import Subject
from app.schemas.creator import CreatorMini
from .base_schema import BaseSchema

if TYPE_CHECKING:
    from app.schemas import (
        Subject,
        CreatorMini,
    )  # noqa: F401


class SearchCompletion(BaseSchema):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    creator: str = Field(..., description="List of authors.")
    title: str = Field(..., description="A human-readable name given to the work.")
    description: Optional[str] = Field(
        None, description="A short, single-sentence summary of the creative work.",
    )

    class Config:
        orm_mode = True

    @validator("creator", pre=True)
    def evaluate_creator(cls, v):
        if isinstance(v, ZeroOrMore):
            creator = [c.creator if c.creator else "Anonymous" for c in v.all()]
            if len(creator) == 1:
                return creator[0]
            if len(creator) == 2:
                return f"{creator[0]} & {creator[1]}"
            return f"{', '.join(creator[:-1])} & {creator[-1]}"
        return "Anonymous"


class SearchSummary(BaseSchema):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    work: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    creator: List[str] = Field(..., description="List of authors.")
    title: str = Field(..., description="A human-readable name given to the work.")
    description: Optional[str] = Field(
        None, description="A short, single-sentence summary of the creative work.",
    )
    long_description: Optional[str] = Field(
        None, description="The pitch, or jacket-cover, description of the creative work.",
    )
    subject: List[str] = Field([], description="A list of topics of the resource.")
    isodate: Optional[date] = Field(
        None, description="The publication date of the creative work. Provide in ISO format, YYYY-MM-DD."
    )
    word_count: Optional[int] = Field(
        None, description="Total word count of the creative work.",
    )

    class Config:
        orm_mode = True

    @validator("work", pre=True)
    def evaluate_work(cls, v):
        if isinstance(v, One):
            return v.single().identifier
        return v

    @validator("creator", pre=True)
    def evaluate_creator(cls, v):
        if isinstance(v, ZeroOrMore):
            return [c.creator if c.creator else "Anonymous" for c in v.all()]
        return ["Anonymous"]

    @validator("subject", pre=True)
    def evaluate_subject(cls, v):
        if isinstance(v, ZeroOrMore):
            return [s.term for s in v.all()]
        return v


class SearchResult(SearchSummary):
    creator: List[CreatorMini] = Field([], description="List of summary creator profiles.")

    class Config:
        orm_mode = True

    @validator("creator", pre=True)
    def evaluate_creator(cls, v):
        if isinstance(v, ZeroOrMore):
            return [CreatorMini.from_orm(c) for c in v.all()]
        return v


SearchSummary.update_forward_refs()
SearchResult.update_forward_refs()
