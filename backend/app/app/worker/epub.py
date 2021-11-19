from raven import Client
from pathlib import Path
import shutil
import base64
from chapisha import CreateWork

from app.core.celery_app import celery_app
from app.core.config import settings
from app.schemas import BuildData

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(name="app.worker.build_epub")
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
    shutil.rmtree(directory)
    return source
