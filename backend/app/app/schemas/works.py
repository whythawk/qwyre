from typing import Optional, List
from pydantic import BaseModel, Field, AnyHttpUrl
from uuid import UUID

from app.schema_types import DCMimeType


class DataUpload(BaseModel):
    mime: DCMimeType
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
