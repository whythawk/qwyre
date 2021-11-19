from enum import auto

from app.schema_types import BaseEnum


class InvitationResponseType(BaseEnum):
    WAITING = auto()
    ACCEPTED = auto()
    REFUSED = auto()
