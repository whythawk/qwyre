from __future__ import annotations
from typing import TYPE_CHECKING
from neomodel import (
    StringProperty,
    UniqueIdProperty,
    DateTimeProperty,
    RelationshipFrom,
    One,
)
from datetime import datetime
import pytz

from app.gdb import NodeBase
from app.schema_types import WorkStateType

if TYPE_CHECKING:
    from app.models import Creator, Work, Series, Anthology, Subscription  # noqa: F401


class Subject(NodeBase):
    identifier = UniqueIdProperty()
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    term = StringProperty(help_text="Optional notes to the state change.",)
    subscribers = RelationshipFrom("app.models.subscriptions.Subscription", "SUBJECT_SUBSCRIBER")
    creator = RelationshipFrom("app.models.creator.Creator", "DESCRIBES_CREATOR", cardinality=One)
    work = RelationshipFrom("app.models.work.Work", "DESCRIBES_WORK", cardinality=One)
    series = RelationshipFrom("app.models.anthology.Series", "DESCRIBES_SERIES", cardinality=One)
    anthology = RelationshipFrom("app.models.anthology.Anthology", "DESCRIBES_ANTHOLOGY", cardinality=One)
