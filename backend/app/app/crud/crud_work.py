from typing import List, Union
from neomodel import db, Q, CardinalityViolation

from app.crud.neo_base import NeoCRUDBase
from app.models import Work, WorkMetadata, Contract, StateHistory
from app.schemas import WorkCreate, WorkUpdate, WorkInDB
from app.schema_types import WorkStateType


class CRUDWork(NeoCRUDBase[Work, WorkCreate, WorkUpdate]):
    @db.write_transaction
    def add_metadata(self, *, db_obj: Work, metadata_obj: WorkMetadata) -> Work:
        try:
            old_metadata_obj = db_obj.metadata.single()
            db_obj.metadata.reconnect(old_node=old_metadata_obj, new_node=metadata_obj)
        except CardinalityViolation:
            db_obj.metadata.connect(metadata_obj)
        return db_obj

    @db.write_transaction
    def add_contract(self, *, db_obj: Work, contract_obj: Contract) -> Work:
        try:
            old_contract_obj = db_obj.contract.single()
            db_obj.contract.reconnect(old_node=old_contract_obj, new_node=contract_obj)
        except CardinalityViolation:
            db_obj.contract.connect(contract_obj)
        return db_obj

    @db.read_transaction
    def get_multi_by_state(self, *, state: WorkStateType, skip: int = 0, limit: int = 100) -> List[Work]:
        db_objs = self.model.nodes.filter(Q(state=state))[skip : limit + skip]
        return self.get_relationships(db_objs)

    @db.read_transaction
    def get_multi_published_by_creator(self, *, skip: int = 0, limit: int = 100) -> List[Work]:
        db_objs = self.model.nodes.filter(Q(state=WorkStateType.PUBLISHED))[skip : limit + skip]
        return self.get_relationships(db_objs)

    @db.read_transaction
    def get_multi_published_by_subject(self, *, skip: int = 0, limit: int = 100) -> List[Work]:
        db_objs = self.model.nodes.filter(Q(state=WorkStateType.PUBLISHED))[skip : limit + skip]
        return self.get_relationships(db_objs)

    @db.write_transaction
    def update_state(self, *, db_obj: Work, history_obj: StateHistory, get_raw: bool = False) -> Work:
        db_obj.contract.connect(history_obj)
        db_obj.state = history_obj.state
        return self._response(db_objs=db_obj, get_raw=get_raw)

    @db.write_transaction
    def withdraw_or_suspend(self, *, db_obj: Work, state_in: WorkStateType, get_raw: bool = False) -> Work:
        if state_in not in [WorkStateType.WITHDRAWN, WorkStateType.SUSPENDED]:
            raise ValueError(f"This function only applies for the withdrawal or suspension of a work.")
        work_in = self.get_relationships(db_objs=db_obj)
        work_in = WorkUpdate(**WorkInDB.from_orm(work_in).dict())
        work_in.state = state_in
        work_in_data = work_in.as_neo_dict
        Work.create_or_update(work_in_data)
        return self._response(db_objs=db_obj, get_raw=get_raw)


work = CRUDWork(Work)
