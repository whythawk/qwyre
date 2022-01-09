from __future__ import annotations
from typing import Optional, Dict, Any, List
from pydantic import Field, validator
from uuid import UUID
from datetime import date
from neomodel.relationship_manager import ZeroOrMore
from neomodel import CardinalityViolation, One

from .base_schema import BaseSchema
from app.schemas.creator import CreatorProfile, CreatorMini
from app.schemas.work import WorkLineSummary


class PartyCreatorCreate(BaseSchema):
    proportion: int = Field(..., description="Proportional share for revenue distribution. Max of 100.")
    isApproved: bool = Field(default=False, description="Party only approved once all parties have approved it.")
    publicationApproved: bool = Field(
        default=False, description="Publication must be approved by the party.",
    )
    creator: Optional[UUID] = Field(None, description="Reference UUID for a creator profile.")


class PartyCreate(BaseSchema):
    proportion: int = Field(..., description="Proportional share for revenue distribution. Max of 100.")
    isApproved: bool = Field(default=False, description="Party only approved once all parties have approved it.")
    publicationApproved: bool = Field(
        default=False, description="Publication must be approved by the party.",
    )


class PartyUpdate(PartyCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    creator: Optional[UUID] = Field(None, description="Reference UUID for a creator profile.")

    class Config:
        orm_mode = True

    @validator("creator", pre=True)
    def evaluate_creator(cls, v):
        if isinstance(v, One):
            try:
                v = v.single()
                return v.identifier
            except CardinalityViolation:
                return None
        return v


class PartyInDB(PartyCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    creator: Optional[CreatorProfile] = Field(None, description="A creator profile.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True

    @validator("creator", pre=True)
    def evaluate_creator(cls, v):
        if isinstance(v, One):
            try:
                return CreatorProfile.from_orm(v.single())
            except CardinalityViolation:
                return None
        return v


class Party(PartyInDB):
    pass


class ContractCreate(BaseSchema):
    isApproved: bool = Field(default=False, description="Contract only approved once all parties have approved it.")
    publicationApproved: bool = Field(
        default=False, description="Publication only approved once all parties have approved it.",
    )
    description: Optional[str] = Field(None, description="Optional notes to the state change.")
    parties: List[PartyCreatorCreate] = Field(
        [], description="List of parties to the contract. At least one required to create."
    )
    work: Optional[UUID] = Field(
        None, description="Creative project governed by this contract. May be any of work, series or anthology."
    )
    series: Optional[UUID] = Field(
        None, description="Creative project governed by this contract. May be any of work, series or anthology."
    )
    anthology: Optional[UUID] = Field(
        None, description="Creative project governed by this contract. May be any of work, series or anthology."
    )

    @validator("anthology")
    def evaluate_anthology(cls, v, values: Dict[str, Any]):
        if not values.get("series") and not values.get("work") and not v:
            raise ValueError("Contract must reference one of work, series or anthology.")
        return v


class ContractUpdate(ContractCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    parties: List[PartyUpdate] = Field(
        [], description="List of parties to the contract. At least one required to create."
    )

    class Config:
        orm_mode = True

    @validator("parties", pre=True)
    def evaluate_parties(cls, v):
        if isinstance(v, ZeroOrMore):
            return [PartyUpdate.from_orm(c) for c in v.all()]
        return v

    @validator("work", "series", "anthology", pre=True)
    def evaluate_work(cls, v):
        if isinstance(v, One):
            try:
                v = v.single()
                return v.identifier
            except CardinalityViolation:
                return None
        return v


class ContractInDB(ContractCreate):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: date = Field(..., description="Automatically generated date resource was created.")
    parties: List[Party] = Field(..., description="Parties to the contract.")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True

    @validator("parties", pre=True)
    def evaluate_parties(cls, v):
        if isinstance(v, ZeroOrMore):
            return [Party.from_orm(c) for c in v.all()]
        return v

    @validator("work", pre=True)
    def evaluate_work(cls, v):
        if isinstance(v, One):
            try:
                return v.single().identifier
            except CardinalityViolation:
                return None
        return v

    @validator("series", pre=True)
    def evaluate_series(cls, v):
        if isinstance(v, One):
            try:
                return v.single().identifier
            except CardinalityViolation:
                return None
        return v

    @validator("anthology", pre=True)
    def evaluate_anthology(cls, v):
        if isinstance(v, One):
            try:
                return v.single().identifier
            except CardinalityViolation:
                return None
        return v


class Contract(ContractInDB):
    work: Optional[WorkLineSummary] = Field(None, description="Work summary, if a work is the subject of this contract")

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        orm_mode = True

    @validator("work", pre=True)
    def evaluate_work(cls, v):
        if isinstance(v, One):
            try:
                return WorkLineSummary.from_orm(v.single())
            except CardinalityViolation:
                return None
        return v


class ContractOffers(Contract):
    offers: List[CreatorMini] = Field([], description="A creator profile.")

    class Config:
        orm_mode = True

    @validator("offers", pre=True)
    def evaluate_offers(cls, v):
        if isinstance(v, ZeroOrMore):
            return [CreatorMini.from_orm(c) for c in v.all()]
        return v


ContractUpdate.update_forward_refs()
Contract.update_forward_refs()
ContractOffers.update_forward_refs()
