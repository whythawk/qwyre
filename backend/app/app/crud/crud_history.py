from typing import List
from neomodel import db, Q, CardinalityViolation

from app.crud.neo_base import NeoCRUDBase
from app.models import StateHistory
from app.schemas import HistoryCreate, HistoryUpdate


class CRUDHistory(NeoCRUDBase[StateHistory, HistoryCreate, HistoryUpdate]):
    pass


party = CRUDHistory(StateHistory)
