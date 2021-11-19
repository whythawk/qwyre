from __future__ import annotations
from typing import Optional, List, Any
from pydantic import Field, EmailStr
from uuid import UUID
from datetime import datetime

from app.schema_types import ResourceType
from .roles import Roles
from .base_schema import BaseSchema


class ResearchResources(BaseSchema):
    resource_id: UUID = Field(..., description="Unique resource identifier.")
    resource_type: ResourceType = Field(
        ..., description="The resource-type referenced.",
    )


class UserInTeam(BaseSchema):
    id: Optional[UUID] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    roles: Optional[List[Roles]] = []

    class Config:
        orm_mode = True


class ResearchTeamBase(BaseSchema):
    title: Optional[str] = Field(None, description="A human-readable name given to the resource.")
    description: Optional[str] = Field(
        None,
        description="A complete description of the resource. Depending on how complex your work becomes, try and be as helpful as possible to 'future-you'. You'll thank yourself later.",
    )
    projects: Optional[List[UUID]] = Field(default=[], description="Projects associated with this team.")
    resources: Optional[List[ResearchResources]] = Field(default=[], description="Resources associated with this team.")
    members: Optional[List[UUID]] = Field(default=[], description="Members of the team.")

    @property
    def as_db_dict(self):
        to_db = self.dict(by_alias=True, exclude_defaults=True, exclude_none=True, exclude={"identifier, id"})
        if "id" in self.dict().keys():
            to_db["id"] = self.dict()["id"].hex
        if "resources" in self.dict().keys() and self.resources:
            to_db["resources"] = [r.as_db_dict for r in self.resources]
        return to_db


class TeamCreate(ResearchTeamBase):
    title: str = Field(..., description="A human-readable name given to the resource.")


class TeamUpdate(ResearchTeamBase):
    pass


class TeamInDBBase(ResearchTeamBase):
    # Identifier managed programmatically
    id: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    title: str = Field(None, description="A human-readable name given to the resource.")
    members: Optional[List[UserInTeam]] = Field(default=[], description="Members of the team.")
    created: datetime = Field(..., description="Automatically generated datetime of creation.")
    updated: Optional[datetime] = Field(None, description="Automatically generated datetime of update.")

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj: Any):
        # Prevent leakage of any member roles from outside of this specific team
        obj_schema = super().from_orm(obj)
        for member in obj_schema.members:
            member.roles = [r for r in member.roles if r.resource_id == obj_schema.id]
        return obj_schema


# Properties to return to client
class Team(TeamInDBBase):
    pass


# Properties properties stored in DB
class TeamInDB(TeamInDBBase):
    pass
