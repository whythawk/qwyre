from typing import List
from neomodel import db, Q, CardinalityViolation

from app.crud.neo_base import NeoCRUDBase
from app.models import WorkMetadata, Contributor, Subject
from app.schemas import WorkMetadataCreate, WorkMetadataUpdate


class CRUDWorkMetadata(NeoCRUDBase[WorkMetadata, WorkMetadataCreate, WorkMetadataUpdate]):
    @db.write_transaction
    def add_subject(self, *, db_obj: WorkMetadata, subject_obj: Subject) -> WorkMetadata:
        db_obj.subject.connect(subject_obj)
        return db_obj

    @db.write_transaction
    def remove_subject(self, *, db_obj: WorkMetadata, subject_obj: Subject) -> WorkMetadata:
        db_obj.subject.disconnect(subject_obj)
        return db_obj

    @db.write_transaction
    def add_contributor(self, *, db_obj: WorkMetadata, contributor_obj: Contributor) -> WorkMetadata:
        db_obj.contributor.connect(contributor_obj)
        return db_obj

    @db.write_transaction
    def remove_contributor(self, *, db_obj: WorkMetadata, contributor_obj: Contributor) -> WorkMetadata:
        db_obj.contributor.disconnect(contributor_obj)
        return db_obj


work_metadata = CRUDWorkMetadata(WorkMetadata)
