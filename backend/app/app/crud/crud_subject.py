from typing import List, Union
from neomodel import db, Q, CardinalityViolation, MultipleNodesReturned

from app.crud.neo_base import NeoCRUDBase
from app.models import Subject
from app.schemas import SubjectCreate, SubjectUpdate


class CRUDSubject(NeoCRUDBase[Subject, SubjectCreate, SubjectUpdate]):
    def create_or_update(self, *, obj_in: SubjectCreate, get_raw: bool = False, get_first: bool = True) -> Subject:
        # SubjectCreate because don't want to deal with identifiers
        try:
            db_obj = Subject.nodes.get_or_none(term=obj_in.term)
        except MultipleNodesReturned:
            db_obj = Subject.nodes.filter(Q(term=obj_in.term)).first()
        if db_obj:
            obj_existing = SubjectUpdate.from_orm(db_obj)
            obj_in = SubjectUpdate(**obj_existing.copy(update=obj_in.dict(exclude_unset=True)).dict())
            return self.update(obj_in=obj_in, get_raw=get_raw, get_first=get_first)
        return self.create(obj_in=obj_in, get_raw=get_raw, get_first=get_first)


subject = CRUDSubject(Subject)
