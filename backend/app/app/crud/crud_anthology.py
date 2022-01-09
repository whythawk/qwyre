from typing import List
from neomodel import db, Q, CardinalityViolation

from app.crud.neo_base import NeoCRUDBase
from app.models import Anthology, Contributor, Contract, StateHistory
from app.schemas import AnthologyCreate, AnthologyUpdate


class CRUDAnthology(NeoCRUDBase[Anthology, AnthologyCreate, AnthologyUpdate]):
    @db.write_transaction
    def add_contract(self, *, db_obj: Anthology, contract_obj: Contract) -> Anthology:
        try:
            old_contract_obj = db_obj.contract.single()
            db_obj.contract.reconnect(old_node=old_contract_obj, new_node=contract_obj)
        except CardinalityViolation:
            db_obj.contract.connect(contract_obj)
        return self.get_relationships(db_obj)

    @db.write_transaction
    def update_state(self, *, db_obj: Anthology, history_obj: StateHistory, get_raw: bool = False) -> Anthology:
        db_obj.contract.connect(history_obj)
        db_obj.state = history_obj.state
        return self._response(db_objs=db_obj, get_raw=get_raw)


party = CRUDAnthology(Anthology)
