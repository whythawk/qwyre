from typing import List
from neomodel import db, Q, CardinalityViolation

from app.crud.neo_base import NeoCRUDBase
from app.models import Party, Contributor
from app.schemas import PartyCreate, PartyCreatorCreate, PartyUpdate


class CRUDParty(NeoCRUDBase[Party, PartyCreate, PartyUpdate]):
    pass


party = CRUDParty(Party)
