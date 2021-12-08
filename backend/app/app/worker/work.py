from raven import Client
from typing import Optional
from pathlib import Path
import shutil
import base64
from uuid import UUID
from neomodel import CardinalityViolation
from chapisha import CreateWork

from app.core.celery_app import celery_app
from app.core.config import settings
from app.schemas import (
    BuildData,
    WorkCreate,
    WorkUpdate,
    WorkMetadataCreate,
    WorkMetadataUpdate,
    ContributorCreate,
    SubjectCreate,
)
from app.schema_types import WorkStateType, ResourceType, MimeType
from app.utilities import StreamFromWork
from app import crud

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(name="app.worker.build_epub")
def build_epub(data: BuildData, identifier: str) -> str:
    directory = Path(settings.WORKING_PATH) / identifier
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


@celery_app.task(name="app.worker.create_or_update_work")
def create_or_update_work(data: BuildData, creator_id: UUID, work_id: Optional[UUID] = None) -> UUID:
    creator = crud.creator.get(id=creator_id, get_raw=True)
    # Create the work & get identifier
    if work_id:
        work = crud.work.get(id=work_id)
        work_in = WorkUpdate.from_orm(work)
        work_in.state = WorkStateType.UPDATED
        if data.get("dedication"):
            work_in.dedication = data.get("dedication")
        work = crud.work.update(obj_in=work_in, get_raw=True)
        # And update any contract as a result of this change
        try:
            crud.contract.reset_on_change(db_obj=work.contract.single())
        except CardinalityViolation:
            pass
    else:
        work_in = WorkCreate(**{"dedication": data.get("dedication"), "state": WorkStateType.SUBMITTED,})
        work = crud.work.create(obj_in=work_in, get_raw=True)
    # Save the epub to Spaces ... create/update are equivalent
    work_name = f"{work.identifier}.epub"
    crud.spaces.create(
        filename=work_name, resource_type=ResourceType.WORK, source=data["work"],
    )
    # Save the cover to Spaces
    cover_name = f"{work.identifier}.img"
    crud.spaces.create(
        filename=cover_name, resource_type=ResourceType.COVER, source=data["cover"],
    )
    # Load work and process to generate stream and summaries
    data["work"] = crud.files.strip_as_epub(source=data["work"])
    crud.files.create(source=data["work"], filetype=MimeType.EPUB, filename=work_name)
    workstream = StreamFromWork()
    workstream_in = workstream.get_work_stream(Path(settings.WORKING_PATH) / work_name)
    work_in = WorkUpdate.from_orm(work)
    work_in = WorkUpdate(**work_in.copy(update=workstream_in.dict(exclude_unset=True)).dict())
    work = crud.work.update(obj_in=work_in, get_raw=True)
    crud.files.remove(filename=work_name)
    # Create Metadata obj
    metadata_id = None
    contributor_in_list = []
    subject_in = []
    metadata_in = workstream_in.metadata  # .dict(exclude_unset=True)
    metadata_uid = metadata_in["identifier"]
    metadata_in["uid"] = workstream_in.metadata.pop("identifier")
    if metadata_in.get("subject"):
        subject_in = metadata_in.pop("subject")
    if metadata_in.get("contributor"):
        contributor_in_list = metadata_in.pop("contributor")
    metadata_in = WorkMetadataCreate(**metadata_in)
    if work_id:
        # If existing work (i.e. provided work_id) then has existing metadata, update it from workstream
        metadata_obj = crud.work_metadata.get_relationships(work.metadata.single())
        metadata_id = UUID(metadata_obj.identifier)
        metadata_existing = WorkMetadataUpdate.from_orm(metadata_obj)
        metadata_in = WorkMetadataUpdate(**metadata_existing.copy(update=workstream_in.metadata).dict())
    if data.get("metadata"):
        # If the creator also provided additional metadata on top of the work metadata ... update from that
        if not data["metadata"].get("uid"):
            data["metadata"]["uid"] = data["metadata"].pop("identifier")
        metadata_extra = WorkMetadataCreate(**data["metadata"])
        if work_id:
            # Update the update
            metadata_in = WorkMetadataUpdate(**metadata_in.copy(update=metadata_extra.dict(exclude_unset=True)).dict())
        else:
            # Update the create
            metadata_in = WorkMetadataCreate(**metadata_in.copy(update=metadata_extra.dict(exclude_unset=True)).dict())
        # Submitted metadata and contributors replaces those from the work itself
        if data["metadata"].get("subject"):
            subject_in = data["metadata"]["subject"]
        if data["metadata"].get("contributor"):
            contributor_in_list = data["metadata"]["contributor"]
    # Assign identifier as UID
    metadata_in.uid = metadata_uid
    # Create or Update
    if metadata_id:
        metadata_in.identifier = metadata_id
        metadata = crud.work_metadata.update(obj_in=metadata_in, get_raw=True)
    else:
        metadata = crud.work_metadata.create(obj_in=metadata_in, get_raw=True)
    # Add any contributors
    for contributor_in in contributor_in_list:
        contributor_in = ContributorCreate(**contributor_in)
        contributor = crud.contributor.create_or_update(obj_in=contributor_in, get_raw=True, get_first=True)
        metadata = crud.work_metadata.add_contributor(db_obj=metadata, contributor_obj=contributor)
    # Add any subjects
    subject_in_list = [s.split("--")[0].strip().lower() for s in subject_in]
    for term in subject_in_list:
        subject_in = SubjectCreate(**{"term": term})
        subject = crud.subject.create_or_update(obj_in=subject_in, get_raw=True, get_first=True)
        metadata = crud.work_metadata.add_subject(db_obj=metadata, subject_obj=subject)
    # Connect other nodes
    work = crud.work.add_metadata(db_obj=work, metadata_obj=metadata)
    crud.creator.add_work(db_obj=creator, work_medata_obj=metadata)
    return work.identifier

