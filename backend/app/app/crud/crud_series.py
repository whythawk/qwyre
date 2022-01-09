from typing import List
from neomodel import db, Q, CardinalityViolation

from app.crud.neo_base import NeoCRUDBase
from app.models import Series, Contributor, Contract, StateHistory
from app.schemas import SeriesCreate, SeriesUpdate


class CRUDSeries(NeoCRUDBase[Series, SeriesCreate, SeriesUpdate]):
    @db.write_transaction
    def add_contract(self, *, db_obj: Series, contract_obj: Contract) -> Series:
        try:
            old_contract_obj = db_obj.contract.single()
            db_obj.contract.reconnect(old_node=old_contract_obj, new_node=contract_obj)
        except CardinalityViolation:
            db_obj.contract.connect(contract_obj)
        return self.get_relationships(db_obj)

    @db.write_transaction
    def update_state(self, *, db_obj: Series, history_obj: StateHistory, get_raw: bool = False) -> Series:
        db_obj.contract.connect(history_obj)
        db_obj.state = history_obj.state
        return self._response(db_objs=db_obj, get_raw=get_raw)


party = CRUDSeries(Series)
