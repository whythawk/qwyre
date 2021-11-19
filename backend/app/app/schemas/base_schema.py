from __future__ import annotations
from pydantic import BaseModel
import json

from app.schema_types import BaseEnum


class BaseSchema(BaseModel):
    @property
    def as_db_dict(self):
        to_db = self.dict(by_alias=True, exclude_defaults=True, exclude_none=True, exclude={"identifier, id"})
        for key in ["id", "identifier"]:
            if key in self.dict().keys():
                to_db[key] = self.dict()[key].hex
        return to_db

    @property
    def as_neo_dict(self):
        to_db = self.json(by_alias=True, exclude_defaults=True, exclude_none=True, exclude={"identifier, id"})
        to_db = json.loads(to_db)
        for key in self.dict().keys():
            if isinstance(self.dict()[key], BaseEnum):
                # Uppercase the Enum values
                to_db[key] = to_db[key].upper()
            if key in ["id", "identifier"]:
                to_db[key] = self.dict()[key].hex
        return to_db
