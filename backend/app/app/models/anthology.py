from __future__ import annotations
from typing import TYPE_CHECKING
from neomodel import (
    UniqueIdProperty,
    StringProperty,
    ArrayProperty,
    IntegerProperty,
    DateProperty,
    DateTimeProperty,
    JSONProperty,
    RelationshipTo,
    RelationshipFrom,
    One,
)
from datetime import datetime
import pytz

from app.gdb import NodeBase, MetadataBase
from app.schema_types import WorkStateType

if TYPE_CHECKING:
    from app.models import Creator, Contributor, Contract, StateHistory, Work, Subscriber  # noqa: F401


class SeriesWorks(NodeBase):
    identifier = UniqueIdProperty()
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    index = IntegerProperty(help_text="Order of the work in the Series.",)
    description = StringProperty(help_text="Optional notes as to why included in the series.",)
    work = RelationshipFrom("app.models.work.Work", "WORK_MEMBER", cardinality=One)
    series = RelationshipFrom("Series", "SERIES_MEMBER", cardinality=One)
    anthology = RelationshipFrom("Anthology", "ANTHOLOGY_MEMBER", cardinality=One)


class Series(MetadataBase):
    works = RelationshipTo("SeriesWorks", "SERIES_MEMBER")
    isodate = DateProperty(help_text="The publication date of the series. Provide in ISO format, YYYY-MM-DD.")
    state = StringProperty(choices=WorkStateType.as_dict(), help_text="The current work state.")
    history = RelationshipTo("app.models.history.StateHistory", "SERIES_WORKFLOW")
    contract = RelationshipTo("app.models.contract.Contract", "SERIES_CONTRACT")
    anthology = RelationshipFrom("Series", "SERIES_RELEASE", cardinality=One)
    curator = RelationshipFrom("app.models.creator.Creator", "CURATED_SERIES")
    subscribers = RelationshipFrom("app.models.subscriptions.Subscriber", "SERIES_SUBSCRIBER")


class Anthology(MetadataBase):
    isodate = DateProperty(help_text="The publication date of the series. Provide in ISO format, YYYY-MM-DD.")
    state = StringProperty(choices=WorkStateType.as_dict(), help_text="The current work state.")
    series = RelationshipTo("Series", "SERIES_RELEASE")
    works = RelationshipTo("SeriesWorks", "ANTHOLOGY_MEMBER")
    history = RelationshipTo("app.models.history.StateHistory", "SERIES_WORKFLOW")
    contract = RelationshipTo("app.models.contract.Contract", "SERIES_CONTRACT")
    curator = RelationshipFrom("app.models.creator.Creator", "CURATED_ANTHOLOGY")
    subscribers = RelationshipFrom("app.models.subscriptions.Subscriber", "ANTHOLOGY_SUBSCRIBER")
