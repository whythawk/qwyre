from typing import Union
from pathlib import Path
import base64
from PIL import Image
from io import BytesIO
from uuid import UUID

from app.core.config import settings
from app.schema_types import MimeType, ResourceType
from app.crud import spaces


class CRUDCover:
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD) working data on the local drive.
        """
        self.directory = Path(settings.WORKING_PATH)
        self.cover_size = 800, 500
        self.thumbnail_size = 200, 125

    def _hexify(self, id: Union[UUID, str]) -> str:
        if isinstance(id, str):
            id = UUID(id)
        return id.hex

    def convert_to_size(self, *, source: BytesIO, size: tuple) -> Image:
        resized_cover = Image.open(source)
        resized_cover.thumbnail(size)
        return resized_cover

    def strip_mimetype(self, *, source: str) -> str:
        if ";base64," in source:
            return source.split(";base64,")[1]
        return source

    def set_mime(self, *, source: str) -> str:
        return "data:image/jpeg;base64," + source.decode("utf-8")

    def convert_to_base64(self, *, source: Image) -> str:
        outputBuffer = BytesIO()
        source = source.convert("RGB")
        source.save(outputBuffer, format="JPEG")
        bgBase64Data = outputBuffer.getvalue()
        return base64.b64encode(bgBase64Data).decode("utf-8")

    def save(self, *, source: str, source_id: UUID):
        source = self.strip_mimetype(source=source)
        source = BytesIO(base64.b64decode(source))
        # Save the cover
        cover = self.convert_to_size(source=source, size=self.cover_size)
        cover = self.convert_to_base64(source=cover)
        spaces.create(
            filename=source_id, resource_type=ResourceType.COVER, source=cover,
        )
        # Save the thumbnail
        thumbnail = self.convert_to_size(source=source, size=self.thumbnail_size)
        thumbnail = self.convert_to_base64(source=thumbnail)
        spaces.create(
            filename=source_id, resource_type=ResourceType.THUMBNAIL, source=thumbnail,
        )

    def get(self, *, source_id: UUID, cover_type: ResourceType) -> str:
        source_id = self._hexify(id=source_id)
        cover = spaces.get(filename=source_id, resource_type=cover_type)
        if not cover:
            return None
        return self.set_mime(source=base64.b64encode(cover))


cover = CRUDCover()
