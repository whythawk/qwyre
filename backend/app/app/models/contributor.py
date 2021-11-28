from __future__ import annotations
from typing import TYPE_CHECKING
from neomodel import StringProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom, One

from app.gdb import NodeBase
from app.schema_types import ContributorRoleType

if TYPE_CHECKING:
    from app.models import Creator, WorkMetadata  # noqa: F401


class Contributor(NodeBase):
    identifier = UniqueIdProperty()
    role = StringProperty(choices=ContributorRoleType.as_dict(), help_text="The role performed by the contributor.")
    name = StringProperty(
        help_text="The public name a contributor wishes to be called. Only needed if the contributor doesn't have an existing creator identity in the database.",
    )
    terms = StringProperty(
        help_text="Information about copyright held by the rights-holder and their terms-of-use for their contribution to the creative work.",
    )
    work = RelationshipFrom("app.models.work.WorkMetadata", "WORK_CONTRIBUTOR", cardinality=One)
    creator = RelationshipFrom("app.models.creator.Creator", "CONTRIBUTED", cardinality=One)

