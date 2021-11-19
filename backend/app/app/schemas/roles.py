from __future__ import annotations
from typing import List
from pydantic import Field
from uuid import UUID

from app.schema_types import ResourceType, ResearcherRoleType
from .base_schema import BaseSchema


class ResourceMemberRolesBase(BaseSchema):
    resource_id: UUID = Field(
        ..., description="Unique identity for the referenced resource",
    )
    resource_type: ResourceType = Field(
        ..., description="The resource-type referenced.",
    )
    researcher_id: UUID = Field(
        ..., description="Specified research team member with responsibility.",
    )
    research_roles: List[ResearcherRoleType] = Field(
        ..., description="A list of roles and rights assigned to this researcher.",
    )


class RolesCreate(ResourceMemberRolesBase):
    pass


class RolesUpdate(ResourceMemberRolesBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class RolesInDBBase(ResourceMemberRolesBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the resource.")

    class Config:
        orm_mode = True


# Properties to return to client
class Roles(RolesInDBBase):
    pass


# Properties properties stored in DB
class RolesInDB(RolesInDBBase):
    pass
