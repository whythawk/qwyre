from __future__ import annotations
from typing import Optional, Dict, Any, TYPE_CHECKING
from pydantic import Field, validator
from uuid import UUID

from app.schema_types import ContributorRoleType
from .base_schema import BaseSchema

if TYPE_CHECKING:
    from app.schemas import CreatorSummary, WorkSummary  # noqa: F401


class ContributorCreate(BaseSchema):
    role: ContributorRoleType = Field(..., description="The role performed by the contributor.")
    name: Optional[str] = Field(
        None,
        description="The public name a contributor wishes to be called. Only needed if the contributor doesn't have an existing creator identity in the database.",
    )
    terms: Optional[str] = Field(
        None,
        description="Information about copyright held by the rights-holder and their terms-of-use for their contribution to the creative work.",
    )

    # @validator("creator")
    # def evaluate_creator(cls, v, values: Dict[str, Any]):
    #     if not values.get("name") and not v:
    #         raise ValueError("Contributor must have either of a named creator, or a linked profile.")
    #     return v


class ContributorUpdate(ContributorCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")

    class Config:
        orm_mode = True


class ContributorInDB(ContributorCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    creator: Optional[CreatorSummary] = Field(None, description="Summary creator profiles.")
    work: WorkSummary = Field(..., description="Reference UUID to creative work.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class Contributor(ContributorInDB):
    pass


from app.schemas.creator import CreatorSummary
from app.schemas.work import WorkSummary

ContributorInDB.update_forward_refs()
Contributor.update_forward_refs()
