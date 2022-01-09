from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from pydantic import Field
from uuid import UUID
from datetime import date

from .base_schema import BaseSchema

if TYPE_CHECKING:
    from app.schemas import WorkSummary  # noqa: F401


class BookmarkCreate(BaseSchema):
    page: int = Field(..., description="Page or chapter number.")
    position: int = Field(..., description="Current text position.")
    paid: Optional[int] = Field(default=0, description="Price paid for reading. In US$ cents.")
    isOwned: bool = Field(default=False, description="Whether the work is owned or not.")
    payment_reference: Optional[str] = Field(None, description="Payment reference, if any.")


class BookmarkUpdate(BookmarkCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")

    class Config:
        orm_mode = True


class BookmarkInDB(BookmarkCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    reading: WorkSummary = Field(..., description="Summary of a creative work.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class Bookmark(BookmarkInDB):
    pass
