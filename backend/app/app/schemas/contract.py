from __future__ import annotations
from typing import Optional, Dict, Any, List
from pydantic import Field, validator
from uuid import UUID
from datetime import date

from .base_schema import BaseSchema


class PartyCreatorCreate(BaseSchema):
    proportion: int = Field(..., description="Proportional share for revenue distribution. Max of 100.")
    isApproved: bool = Field(default=False, description="Party only approved once all parties have approved it.")
    creator: Optional[UUID] = Field(None, description="Reference UUID for a creator profile.")


class PartyCreate(BaseSchema):
    proportion: int = Field(..., description="Proportional share for revenue distribution. Max of 100.")
    isApproved: bool = Field(default=False, description="Party only approved once all parties have approved it.")


class PartyUpdate(PartyCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class PartyInDB(PartyCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    creator: UUID = Field(..., description="Reference UUID for a creator profile.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class Party(PartyInDB):
    pass


class ContractCreate(BaseSchema):
    isApproved: bool = Field(default=False, description="Contract only approved once all parties have approved it.")
    description: Optional[str] = Field(None, description="Optional notes to the state change.")

    # @validator("anthology")
    # def evaluate_anthology(cls, v, values: Dict[str, Any]):
    #     if not values.get("series") and not values.get("work") and not v:
    #         raise ValueError("Contract must reference one of work, series or anthology.")
    #     return v


class ContractUpdate(ContractCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class ContractInDB(ContractCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    parties: List[PartyInDB] = Field(..., description="Parties to the contract.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True


class Contract(ContractInDB):
    pass


ContractUpdate.update_forward_refs()
Contract.update_forward_refs()
