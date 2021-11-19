from typing import Optional
from pydantic import BaseModel, Field, ValidationError

from chapisha import WorkMetadata

class BuildData(BaseModel):
    metadata: WorkMetadata = Field(...)
    cover: str = Field(...)
    text: str = Field(...)
    dedication: Optional[list[str]] = Field(None)