from typing import List, Union
from neomodel import db, Q, CardinalityViolation, MultipleNodesReturned

from app.crud.neo_base import NeoCRUDBase
from app.models import Contributor, Creator, Work, User
from app.schemas import ContributorCreate, ContributorUpdate
from app.schema_types import ContributorRoleType


class CRUDContributor(NeoCRUDBase[Contributor, ContributorCreate, ContributorUpdate]):
    def has_appropriate_rights(
        self,
        *,
        creator_obj: Creator,
        work_obj: Work,
        user_obj: User,
        roles: Union[List[ContributorRoleType], ContributorRoleType],
    ) -> bool:
        if not isinstance(roles, list):
            roles = [roles]
        if user_obj.is_superuser:
            return True
        if ContributorRoleType.MODERATOR in [roles] and user_obj.is_moderator:
            return True
        if ContributorRoleType.AUTHOR in [roles] and creator_obj.works.get_or_none(
            identifier=work_obj.metadata.single().identifier
        ):
            return True
        contributor_roles = set(
            [
                ContributorRoleType(contributor.role)
                for contributor in work_obj.metadata.single().contributor.all()
                if contributor.creator.single().identifier == creator_obj.identifier
            ]
        )
        if contributor_roles and not set(roles).isdisjoint(contributor_roles):
            return True
        return False

    def create_or_update(
        self, *, obj_in: ContributorCreate, get_raw: bool = False, get_first: bool = True
    ) -> Contributor:
        # ContributorCreate because don't want to deal with identifiers
        try:
            db_obj = Contributor.nodes.get_or_none(name=obj_in.name)
        except MultipleNodesReturned:
            db_obj = Contributor.nodes.filter(Q(name=obj_in.name)).first()
        if db_obj:
            obj_existing = ContributorUpdate.from_orm(db_obj)
            obj_in = ContributorUpdate(**obj_existing.copy(update=obj_in.dict(exclude_unset=True)).dict())
            return self.update(obj_in=obj_in, get_raw=get_raw, get_first=get_first)
        return self.create(obj_in=obj_in, get_raw=get_raw, get_first=get_first)


contributor = CRUDContributor(Contributor)
