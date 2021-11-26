from __future__ import annotations
from typing import TYPE_CHECKING
from neomodel import UniqueIdProperty, IntegerProperty, DateTimeProperty, RelationshipTo, RelationshipFrom, One
from datetime import datetime
import pytz

from app.gdb import NodeBase

if TYPE_CHECKING:
    from app.models import Creator, Work, Series  # noqa: F401


class Subscription(NodeBase):
    identifier = UniqueIdProperty()
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    index = IntegerProperty(help_text="Order of the subscription (optional)",)
    subscriber = RelationshipFrom("app.models.creator.Creator", "SUBSCRIBES")
    creator = RelationshipFrom("app.models.creator.Creator", "CREATOR_SUBSCRIBER", cardinality=One)
    series = RelationshipFrom("app.models.anthology.Series", "SERIES_SUBSCRIBER", cardinality=One)
    anthology = RelationshipTo("app.models.anthology.Anthology", "ANTHOLOGY_SUBSCRIBER", cardinality=One)
