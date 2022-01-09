from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from pydantic import Field, validator
from uuid import UUID
from neomodel import One

from app.schemas.work import WorkMetadataLineSummary
from .base_schema import BaseSchema


class RevenueShare(BaseSchema):
    proportion: float = Field(..., description="Proportional share for revenue distribution. Max of 1.")
    wallet: Optional[str] = Field(None, description="Payment pointer for web monetization.")


class StreamFirst(BaseSchema):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    metadata: WorkMetadataLineSummary = Field(..., description="Subset of metadata from work.")
    spine: Optional[List[str]] = Field(
        [], description="Spine list of contents for the creative work.",
    )
    first500: Optional[str] = Field(None, description="First 500 words (approx.) of first chapter of creative work.")
    stream: Optional[List[List[str]]] = Field(
        [],
        description="Creative work structured for streaming. Structured as list of pages, containing lists of tags and words.",
    )
    start_page: Optional[int] = Field(
        default=0, description="Starting chapter for stream.",
    )
    page: int = Field(default=0, description="Last page or chapter number.")
    position: int = Field(default=0, description="Last text position.")
    paid: int = Field(default=0, description="Price paid for reading. In US$ cents.")

    class Config:
        orm_mode = True

    @validator("metadata", pre=True)
    def evaluate_metadata(cls, v):
        if isinstance(v, One):
            return WorkMetadataLineSummary.from_orm(v.single())
        return v


class StreamSecond(BaseSchema):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    stream: Optional[List[List[str]]] = Field(
        [],
        description="Creative work structured for streaming. Structured as list of pages, containing lists of tags and words.",
    )
    page: int = Field(..., description="Last page or chapter number.")
    position: int = Field(..., description="Last text position.")
    paid: Optional[int] = Field(None, description="Price paid for reading. In US$ cents.")


StreamFirst.update_forward_refs()
