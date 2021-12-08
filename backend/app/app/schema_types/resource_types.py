from enum import auto

from app.schema_types import BaseEnum


class ResourceType(BaseEnum):
    WORK = auto()
    SOURCE = auto()
    COVER = auto()
