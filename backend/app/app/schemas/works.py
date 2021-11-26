from typing import Optional, List
from pydantic import BaseModel, Field, AnyHttpUrl
from uuid import UUID
from chapisha import WorkMetadata

from app.schema_types import MimeType
from .base_schema import BaseSchema


class DataUpload(BaseModel):
    mime: MimeType
    data: bytes
    name: Optional[str]


class DatasourceUpload(BaseModel):
    data: List[DataUpload] = Field(..., description="A list of base64-encoded data sources.")
    urls: Optional[List[AnyHttpUrl]] = Field([], description="An optional list of urls to individual source files.")
    directory: Optional[AnyHttpUrl] = Field(None, description="An optional link to a source directory.")


class DataSummary(BaseModel):
    name: str
    sheet_name: Optional[str]
    uuid: UUID
    data: Optional[List[dict]]
    row_count: Optional[int]


class WorkSource(BaseModel):
    metadata: Optional[WorkMetadata] = Field(
        None, description="Subset of metadata from work.",
    )
    cover: Optional[str] = Field(
        None, description="Work cover.",
    )
    stream: Optional[List[List[str]]] = Field(
        [], description="Text stream, with sections split into individual words and tags.",
    )
    spine: Optional[List[str]] = Field(
        [], description="Spine titles matching stream list.",
    )
    start_page: Optional[int] = Field(
        default=0, description="Start reading from this point.",
    )

