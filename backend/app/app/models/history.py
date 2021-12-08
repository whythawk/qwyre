from __future__ import annotations
from typing import TYPE_CHECKING
from neomodel import (
    StringProperty,
    UniqueIdProperty,
    BooleanProperty,
    DateTimeProperty,
    RelationshipFrom,
    One,
)
from datetime import datetime
import pytz

from app.gdb import NodeBase
from app.schema_types import WorkStateType

if TYPE_CHECKING:
    from app.models import Creator, Work, Series, Anthology  # noqa: F401


class StateHistory(NodeBase):
    identifier = UniqueIdProperty()
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    expires = DateTimeProperty(help_text="Expiry datetime for this state. Only valid for certain states, e.g. OFFERED.")
    state = StringProperty(choices=WorkStateType.as_dict(), help_text="The work state.")
    description = StringProperty(help_text="Optional notes to the state change.",)
    curator = RelationshipFrom("app.models.creator.Creator", "CURATION_HISTORY", cardinality=One)
    work = RelationshipFrom("app.models.work.Work", "WORKFLOW", cardinality=One)
    series = RelationshipFrom("app.models.anthology.Series", "SERIES_WORKFLOW", cardinality=One)
    anthology = RelationshipFrom("app.models.anthology.Anthology", "ANTHOLOGY_WORKFLOW", cardinality=One)
    creator = RelationshipFrom("app.models.creator.Creator", "MODERATION_WORKFLOW")
