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
    from app.models import Subject, Creator, Contributor, Contract, StateHistory, SeriesWorks, Bookmark  # noqa: F401


class WorkMetadata(MetadataBase):
    subject = RelationshipTo("app.models.subject.Subject", "DESCRIBES_WORK")
    isodate = DateProperty(help_text="The publication date of the creative work. Provide in ISO format, YYYY-MM-DD.")
    language = StringProperty(
        help_text="Specify the language of the creative work. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    long_rights = ArrayProperty(
        StringProperty(
            help_text="Information about copyright held in and over the creative work. Formatted as you wish it to appear.",
        )
    )
    publisher = StringProperty(
        help_text="Name of a person, organisation, etc.  responsible for making the creative work available.",
    )
    publisher_uri = StringProperty(help_text="The URI for your creative work.",)
    work_uri = StringProperty(help_text="The URI for the publisher of your creative work.",)
    word_count = IntegerProperty(help_text="Total word count of your creative work.",)
    creator = RelationshipFrom("app.models.creator.Creator", "AUTHORED")
    contributor = RelationshipTo("app.models.contributor.Contributor", "WORK_CONTRIBUTOR")
    work = RelationshipFrom("Work", "DESCRIBED_BY", cardinality=One)


class Work(NodeBase):
    identifier = UniqueIdProperty()
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    metadata = RelationshipTo("WorkMetadata", "DESCRIBED_BY", cardinality=One)
    dedication = ArrayProperty(StringProperty(help_text="Work dedication. Formatted as you wish it to appear.",))
    price = IntegerProperty(help_text="Maximum price to be charged for reading. In US$ cents.")
    stream = JSONProperty(
        help_text="Creative work structured for streaming. Structured as list of pages, containing lists of tags and words."
    )
    first500 = StringProperty(help_text="First 500 words (approx.) of first chapter of creative work.",)
    start_page = IntegerProperty(help_text="Starting chapter for stream.",)
    spine = ArrayProperty(StringProperty(help_text="Spine list of contents for the creative work.",))
    state = StringProperty(choices=WorkStateType.as_dict(), help_text="The current work state.")
    history = RelationshipTo("app.models.history.StateHistory", "WORKFLOW")
    contract = RelationshipTo("app.models.contract.Contract", "WORK_CONTRACT")
    member = RelationshipFrom("app.models.anthology.SeriesWorks", "WORK_MEMBER")
    reader = RelationshipFrom("app.models.bookmark.Bookmark", "READING")
