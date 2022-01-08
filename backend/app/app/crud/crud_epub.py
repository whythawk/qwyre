from typing import Union
from pathlib import Path
import base64
from io import BytesIO
from uuid import UUID

from app.core.config import settings
from app.schema_types import MimeType, ResourceType
from app.crud import spaces


class CRUDEpub:
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD) working data on the local drive.
        """
        self.directory = Path(settings.WORKING_PATH)

    def _hexify(self, id: Union[UUID, str]) -> str:
        if isinstance(id, str):
            id = UUID(id)
        return id.hex

    def strip_mimetype(self, *, source: str) -> str:
        if source.startswith("data:application/epub+zip;base64,"):
            return source.split("data:application/epub+zip;base64,")[1]
        return source

    def set_mime(self, *, source: str) -> str:
        try:
            return "data:application/epub+zip;base64," + source.decode("utf-8")
        except AttributeError:
            return "data:application/epub+zip;base64," + source

    def convert_to_base64(self, *, source: str) -> str:
        return base64.b64encode(source).decode("utf-8")

    def save(self, *, source: str, source_id: UUID):
        source = self.strip_mimetype(source=source)
        spaces.create(
            filename=source_id, resource_type=ResourceType.WORK, source=source,
        )

    def get(self, *, source_id: UUID) -> str:
        source_id = self._hexify(id=source_id)
        work = spaces.get(filename=source_id, resource_type=ResourceType.WORK)
        if not work:
            return None
        return self.set_mime(source=base64.b64encode(work))


epub = CRUDEpub()
