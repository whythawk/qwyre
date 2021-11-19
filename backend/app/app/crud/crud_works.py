from typing import List, Optional
from pathlib import Path
import shutil
from uuid import uuid4
import base64

from app.core.config import settings
from app.schemas.base_schema import BaseSchema
from app.schema_types import DCMimeType


class CRUDWorks:
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD) working data on the local drive.
        """
        self.directory = Path(settings.WORKING_PATH)

    def create(
        self,
        *,
        source: str,
        filetype: DCMimeType,
        filename: Optional[str] = None,
        subdirectory: Optional[str] = None,
        decoded: bool = False,
    ) -> str:
        # Comes from API, so is always a base64 ... causes challenges with mimetypes ...
        data = source
        if not decoded:
            data = base64.b64decode(source)
        if not filename:
            filename = f"{uuid4()}.{filetype.name}"
        directory = self.directory
        if subdirectory:
            # subdirectory must be of form: '{term}/{term}'
            directory = directory / subdirectory
            Path(directory).mkdir(parents=True, exist_ok=True)
        with open(directory / filename, "wb") as f:
            f.write(data)
        return filename

    def remove(self, *, filename: str, subdirectory: Optional[str] = None):
        directory = self.directory
        if subdirectory:
            directory = directory / subdirectory
        # https://stackoverflow.com/a/42641792/295606
        (directory / filename).unlink(missing_ok=True)

    def remove_directory(self, *, directory: str):
        shutil.rmtree(self.directory / directory, ignore_errors=True)


works = CRUDWorks()
