from typing import List
from neomodel import db, Q
from uuid import UUID

from app.crud.neo_base import NeoCRUDBase
from app.crud.crud_party import party as crud_party
from app.models import Creator, Work, WorkMetadata, Party, StateHistory, Contributor, Subject, User, Contract
from app.schemas import CreatorCreate, CreatorUpdate, CreatorInDB, PartyUpdate, PartyInDB


class CRUDCreator(NeoCRUDBase[Creator, CreatorCreate, CreatorUpdate]):
    def can_make_offers(self, *, db_obj: Creator, user_obj: User) -> bool:
        if not db_obj.isPrivate and not db_obj.isBanned and user_obj.email_validated:
            return True
        return False

    def creator_name(self, *, db_obj: Creator) -> str:
        if db_obj.creator:
            return db_obj.creator
        return "Anonymous"

    @db.write_transaction
    def add_work(self, *, db_obj: Creator, work_medata_obj: WorkMetadata) -> Creator:
        db_obj.works.connect(work_medata_obj)
        return self.get_relationships(db_obj)

    @db.write_transaction
    def add_subject(self, *, db_obj: Creator, subject_obj: Subject) -> WorkMetadata:
        db_obj.subject.connect(subject_obj)
        return self.get_relationships(db_obj)

    @db.write_transaction
    def remove_subject(self, *, db_obj: Creator, subject_obj: Subject) -> WorkMetadata:
        db_obj.subject.disconnect(subject_obj)
        return self.get_relationships(db_obj)

    @db.write_transaction
    def add_contribution(self, *, db_obj: Creator, contributor_obj: Contributor) -> Creator:
        db_obj.contributor.connect(contributor_obj)
        return self.get_relationships(db_obj)

    @db.write_transaction
    def remove_contribution(self, *, db_obj: Creator, contributor_obj: Contributor) -> Creator:
        db_obj.contributor.disconnect(contributor_obj)
        return self.get_relationships(db_obj)

    @db.write_transaction
    def add_contract(self, *, db_obj: Creator, party_obj: Party) -> Creator:
        db_obj.contracts.connect(party_obj)
        return self.get_relationships(db_obj)

    @db.write_transaction
    def remove_contract(self, *, db_obj: Creator, party_obj: Party) -> Creator:
        db_obj.contracts.disconnect(party_obj)
        return self.get_relationships(db_obj)

    @db.write_transaction
    def add_contract_offer(self, *, db_obj: Creator, contract_obj: Contract) -> Creator:
        db_obj.offers.connect(contract_obj)
        return self.get_relationships(db_obj)

    @db.write_transaction
    def remove_contract_offer(self, *, db_obj: Creator, contract_obj: Contract) -> Creator:
        db_obj.offers.disconnect(contract_obj)
        return self.get_relationships(db_obj)

    @db.write_transaction
    def toggle_privacy(self, *, db_obj: Creator, get_raw: bool = False, get_first: bool = True) -> Creator:
        obj_in = CreatorUpdate(**CreatorInDB.from_orm(db_obj).dict())
        # neo_dict wrecks booleans ...
        obj_in_data = obj_in.as_neo_dict
        obj_in_data["isPrivate"] = not db_obj.isPrivate
        db_obj = self.model.create_or_update(obj_in_data)  # type: ignore
        return self._response(db_objs=db_obj, get_raw=get_raw, get_first=get_first)

    @db.write_transaction
    def approve_contract(
        self, *, db_obj: Creator, party_id: UUID, for_contract: bool = True, get_raw: bool = False
    ) -> Creator:
        # Done this way to be absolutely certain that a creator may ONLY approve their own role
        # in a contract or publication.
        contract_obj = db_obj.contracts.get(identifier=self._hexify(party_id))
        party_in = crud_party.get_relationships(db_objs=contract_obj)
        party_in = PartyUpdate(**PartyInDB.from_orm(party_in).dict())
        if for_contract:
            party_in.isApproved = True
        else:
            party_in.publicationApproved = True
        party_in_data = party_in.as_neo_dict
        Party.create_or_update(party_in_data)
        return self._response(db_objs=db_obj, get_raw=get_raw)

    @db.write_transaction
    def revoke_contract_approval(
        self, *, db_obj: Creator, party_id: UUID, for_contract: bool = True, get_raw: bool = False
    ) -> Creator:
        # Done this way to be absolutely certain that a creator may ONLY approve their own role
        # in a contract or publication.
        contract_obj = db_obj.contracts.get(identifier=self._hexify(party_id))
        party_in = crud_party.get_relationships(db_objs=contract_obj)
        party_in = PartyUpdate(**PartyInDB.from_orm(party_in).dict())
        if for_contract:
            party_in.isApproved = False
        else:
            party_in.publicationApproved = False
        party_in_data = party_in.as_neo_dict
        Party.create_or_update(party_in_data)
        return self._response(db_objs=db_obj, get_raw=get_raw)

    @db.read_transaction
    def get_multi_works(self, *, db_obj: Creator, skip: int = 0, limit: int = 100, get_raw: bool = False) -> List[Work]:
        db_objs = db_obj.works.all()[skip : limit + skip]
        db_objs = [o.work.single() for o in db_objs]
        return self._response(db_objs=db_objs, get_raw=get_raw, get_first=False)

    @db.read_transaction
    def get_work(self, *, db_obj: Creator, work_id: UUID, get_raw: bool = False) -> Work:
        db_obj = db_obj.works.get_or_none(identifier=self._hexify(work_id))
        if not db_obj:
            return db_obj
        db_obj = db_obj.work.single()
        return self._response(db_objs=db_obj, get_raw=get_raw)

    @db.read_transaction
    def get_multi_public(self, *, skip: int = 0, limit: int = 100) -> List[Creator]:
        db_objs = self.model.nodes.filter(Q(isPrivate=False) & Q(isActive=True) & Q(isBanned=False))[
            skip : limit + skip
        ]
        return self.get_relationships(db_objs)

    @db.write_transaction
    def add_curation_history(self, *, db_obj: Creator, history_obj: StateHistory, get_raw: bool = False) -> Creator:
        db_obj.contract.connect(history_obj)
        return self._response(db_objs=db_obj, get_raw=get_raw)


creator = CRUDCreator(Creator)
