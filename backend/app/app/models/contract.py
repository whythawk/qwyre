from __future__ import annotations
from typing import TYPE_CHECKING
from neomodel import (
    BooleanProperty,
    StringProperty,
    UniqueIdProperty,
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
    from app.models import Creator, Work, Series, Anthology  # noqa: F401


class Party(NodeBase):
    identifier = UniqueIdProperty()
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    proportion = IntegerProperty(help_text="Proportional share for revenue distribution. Max of 100.",)
    isApproved = BooleanProperty(default=False, help_text="Contract must be approved by the party.",)
    publicationApproved = BooleanProperty(default=False, help_text="Publication must be approved by the party.",)
    creator = RelationshipFrom("app.models.creator.Creator", "CONTRACTS", cardinality=One)
    contract = RelationshipFrom("Contract", "PARTIES", cardinality=One)


class Contract(NodeBase):
    identifier = UniqueIdProperty()
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    parties = RelationshipTo("Party", "PARTIES")
    isApproved = BooleanProperty(default=False, help_text="Contract only approved once all parties have approved it.",)
    publicationApproved = BooleanProperty(
        default=False, help_text="Publication only approved once all parties have approved it.",
    )
    description = StringProperty(help_text="Optional notes to the contract.",)
    work = RelationshipFrom("app.models.work.Work", "WORK_CONTRACT", cardinality=One)
    series = RelationshipFrom("app.models.anthology.Series", "SERIES_CONTRACT", cardinality=One)
    anthology = RelationshipFrom("app.models.anthology.Anthology", "ANTHOLOGY_CONTRACT", cardinality=One)

