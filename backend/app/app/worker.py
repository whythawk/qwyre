from raven import Client

from app.core.celery_app import celery_app
from app.core.config import settings
from pydantic import BaseModel, Field
from typing import Optional
from chapisha import WorkMetadata, CreateWork
from pathlib import Path
import shutil
import asyncio
import base64

client_sentry = Client(settings.SENTRY_DSN)


class BuildData(BaseModel):
    metadata: WorkMetadata = Field(...)
    cover: str = Field(...)
    text: str = Field(...)
    dedication: Optional[list[str]] = Field(None)


@celery_app.task(acks_late=True)
async def test_celery(word: str) -> str:
    await asyncio.sleep(5)
    return f"test task return {word}"


@celery_app.task
def build_epub(data: BuildData, identifier: str) -> str:
    directory = Path("/app/temp_build") / identifier
    Path(directory).mkdir(parents=True, exist_ok=True)
    work = CreateWork(directory=directory, metadata=data["metadata"])
    work.set_document(data["text"])
    work.set_cover(data["cover"])
    if "dedication" in data:
        work.set_dedication(data["dedication"])
    work.build()
    # Import the epub and convert to base64
    if work.validate():
        with open(directory / f"{work.work_name}.epub", "rb") as EPUB:
            source = base64.b64encode(EPUB.read())
        # Convert to string
        source = "data:application/epub+zip;base64," + source.decode("utf-8")
    else:
        source = "Build failed"
    # shutil.rmtree(directory)
    return source
