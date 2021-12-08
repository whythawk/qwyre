from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class WorkStreamCreate(BaseModel):
    metadata: Optional[Dict] = Field(
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
    first500: Optional[str] = Field(None, description="First 500 words (approx.) of first chapter of creative work.")
    start_page: Optional[int] = Field(
        default=0, description="Start reading from this point.",
    )
