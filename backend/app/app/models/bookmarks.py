from __future__ import annotations
from typing import TYPE_CHECKING
from neomodel import (
    UniqueIdProperty,
    StringProperty,
    IntegerProperty,
    DateTimeProperty,
    RelationshipTo,
    RelationshipFrom,
    One,
)
from datetime import datetime
import pytz

from app.gdb import NodeBase

if TYPE_CHECKING:
    from app.models import Creator, Work  # noqa: F401


class Bookmark(NodeBase):
    identifier = UniqueIdProperty()
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    reader = RelationshipFrom("app.models.creator.Creator", "BOOKMARK", cardinality=One)
    reading = RelationshipTo("app.models.work.Work", "READING", cardinality=One)
    page = IntegerProperty(help_text="Page or chapter number.")
    position = IntegerProperty(help_text="Current text position.")
    paid = IntegerProperty(help_text="Price pad for reading. In US$ cents.")
    payment_reference = StringProperty(help_text="Payment reference, if any.")
