from __future__ import annotations
from typing import TYPE_CHECKING
from neomodel import StringProperty, RelationshipTo

from app.gdb import MetadataBase

if TYPE_CHECKING:
    from app.models import (
        WorkMetadata,
        Contributor,
        StateHistory,
        Series,
        Anthology,
        Subscriber,
        Bookmark,
    )  # noqa: F401


class Creator(MetadataBase):
    creator = StringProperty(help_text="The public name a creator wishes to be called.")
    wallet = StringProperty(help_text="Payment pointer for web monetization.")
    contributor = RelationshipTo("app.models.contributor.Contributor", "CONTRIBUTED")
    works = RelationshipTo("app.models.work.WorkMetadata", "AUTHORED")
    series = RelationshipTo("app.models.anthology.Series", "CURATED_SERIES")
    anthologies = RelationshipTo("app.models.anthology.Anthology", "CURATED_ANTHOLOGY")
    curations = RelationshipTo("app.models.history.StateHistory", "CURATED_STATE")
    subscriptions = RelationshipTo("app.models.subscriptions.Subscriber", "SUBSCRIBES")
    reading = RelationshipTo("app.models.bookmarks.Bookmark", "BOOKMARK")
