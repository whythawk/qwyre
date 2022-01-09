from __future__ import annotations
from typing import TYPE_CHECKING
from neomodel import StringProperty, BooleanProperty, RelationshipTo, RelationshipFrom

from app.gdb import MetadataBase

if TYPE_CHECKING:
    from app.models import (
        WorkMetadata,
        Contributor,
        Contract,
        StateHistory,
        Series,
        Anthology,
        Subscription,
        Subject,
        Bookmark,
    )  # noqa: F401


class Creator(MetadataBase):
    creator = StringProperty(help_text="The public name a creator wishes to be called.")
    wallet = StringProperty(help_text="Payment pointer for web monetization.")
    website = StringProperty(help_text="Creator's personal website")
    contributor = RelationshipTo("app.models.contributor.Contributor", "CONTRIBUTED")
    subject = RelationshipTo("app.models.subject.Subject", "DESCRIBES_CREATOR")
    works = RelationshipTo("app.models.work.WorkMetadata", "AUTHORED")
    series = RelationshipTo("app.models.anthology.Series", "CURATED_SERIES")
    anthologies = RelationshipTo("app.models.anthology.Anthology", "CURATED_ANTHOLOGY")
    curations = RelationshipTo("app.models.history.StateHistory", "CURATION_HISTORY")
    subscriptions = RelationshipTo("app.models.subscriptions.Subscription", "SUBSCRIBES")
    subscribers = RelationshipFrom("app.models.subscriptions.Subscription", "CREATOR_SUBSCRIBER")
    reading = RelationshipTo("app.models.bookmarks.Bookmark", "BOOKMARK")
    isBanned = BooleanProperty(default=False, help_text="This creator crossed the line.",)
    history = RelationshipTo("app.models.history.StateHistory", "MODERATION_WORKFLOW")
    contracts = RelationshipTo("app.models.contract.Party", "CONTRACTS")
    offers = RelationshipTo("app.models.contract.Contract", "INTERESTED")
