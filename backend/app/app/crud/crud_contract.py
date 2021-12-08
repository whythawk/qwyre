from typing import List, Union, Optional
from neomodel import db, Q
from uuid import UUID

from app.crud.neo_base import NeoCRUDBase
from app.crud.crud_party import party as crud_party
from app.models import Party, Contract, Creator
from app.schemas import (
    ContractCreate,
    ContractUpdate,
    ContractInDB,
    PartyCreatorCreate,
    PartyCreate,
    PartyUpdate,
    PartyInDB,
)
from app.schema_types import WorkStateType


class CRUDContract(NeoCRUDBase[Contract, ContractCreate, ContractUpdate]):
    def _check_parties_unique(
        self, *, db_obj: Optional[Contract] = None, parties_in: Union[List[PartyCreatorCreate], PartyCreatorCreate]
    ) -> bool:
        # Check if parties unique
        # https://stackoverflow.com/a/5281641/295606
        if isinstance(parties_in, PartyCreatorCreate):
            parties_in = [parties_in]
        check_list = [self._hexify(party.creator) for party in parties_in if party.creator]
        if len(check_list) > len(set(check_list)):
            return False
        if db_obj:
            seen = set(check_list)
            if any(
                party_obj.creator.identifier in seen or seen.add(party_obj.creator.identifier)
                for party_obj in db_obj.parties
                if party_obj.creator
            ):
                # Not unique
                return False
        return True

    def _check_party_proportions(
        self,
        *,
        db_obj: Contract,
        parties_in: Union[List[PartyCreatorCreate], PartyCreatorCreate, List[PartyUpdate], PartyUpdate],
    ) -> bool:
        if not isinstance(parties_in, list):
            parties_in = [parties_in]
        if not any(party.proportion >= 1 for party in parties_in):
            return False
        proportion_sum = sum([party.proportion for party in parties_in])
        if db_obj:
            if not any(party.proportion >= 1 for party in db_obj.parties):
                return False
            proportion_sum += sum([party.proportion for party in db_obj.parties])
        return proportion_sum == 100

    def _add_parties(self, *, db_obj: Contract, parties_in: List[PartyCreatorCreate]) -> Contract:
        for party_in in parties_in:
            creator = None
            if party_in.creator:
                creator = Creator.nodes.get_or_none(identifier=self._hexify(party_in.creator))
                if not creator:
                    raise ValueError(f"Creator {party_in.creator} does not exist.")
            party_in = PartyCreate(**party_in.dict())
            party_in_data = party_in.as_neo_dict
            party_obj = Party.create_or_update(party_in_data)[0]
            if creator:
                creator.contracts.connect(party_obj)
            db_obj.parties.connect(party_obj)
        return db_obj

    @db.write_transaction
    def create(
        self,
        *,
        obj_in: ContractCreate,
        parties_in: Union[List[PartyCreatorCreate], PartyCreatorCreate],
        get_raw: bool = False,
    ) -> Contract:
        if isinstance(parties_in, PartyCreatorCreate):
            parties_in = [parties_in]
        if not self._check_parties_unique(parties_in=parties_in):
            # Not unique
            raise ValueError("Parties to the contract must be unique.")
        if self._check_party_proportions(parties_in=parties_in):
            # Not an offer
            raise ValueError("Legitimate offer required.")
        # Create the contract and assign the parties to the contract
        obj_in_data = obj_in.as_neo_dict
        db_obj = self.model.create_or_update(obj_in_data)[0]
        db_obj = self._add_parties(db_obj=db_obj, parties_in=parties_in)
        if get_raw:
            return db_obj
        return self.get_relationships(db_obj)

    def validate_contract(self, *, db_obj: Contract) -> bool:
        return all(party.isApproved for party in db_obj.parties)

    def validate_publication(self, *, db_obj: Contract) -> bool:
        return all(party.publicationApproved for party in db_obj.parties)

    @db.write_transaction
    def reset_on_change(self, *, db_obj: Contract, get_raw: bool = False) -> Contract:
        for party in db_obj.parties:
            party_in = crud_party.get_relationships(db_objs=party)
            party_in = PartyUpdate(**PartyInDB.from_orm(party_in).dict())
            party_in.isApproved = False
            party_in.publicationApproved = False
            party_in_data = party_in.as_neo_dict
            Party.create_or_update(party_in_data)
        return self._response(db_objs=db_obj, get_raw=get_raw)

    @db.write_transaction
    def add_parties(
        self,
        *,
        db_obj: Contract,
        parties_in: Union[List[PartyCreatorCreate], PartyCreatorCreate],
        get_raw: bool = False,
    ) -> Contract:
        if isinstance(parties_in, PartyCreatorCreate):
            parties_in = [parties_in]
        if not self._check_parties_unique(db_obj=db_obj, parties_in=parties_in):
            # Not unique
            raise ValueError("Parties to the contract must be unique.")
        if self._check_party_proportions(db_obj=db_obj, parties_in=parties_in):
            # Not an offer
            raise ValueError("Legitimate offer required.")
        db_obj = self._add_parties(db_obj=db_obj, parties_in=parties_in)
        if get_raw:
            return db_obj
        return self.get_relationships(db_obj)

    def update_party_proportions(
        self, *, db_obj: Contract, parties_in: List[PartyUpdate], get_raw: bool = False,
    ) -> Contract:
        contract_parties = {party.identifier: party for party in db_obj.parties}
        updated_parties = {party.identifier: party for party in parties_in}
        if set(contract_parties.keys()).difference(set(updated_parties.keys())):
            # Not unique or complete
            raise ValueError("Parties to the contract must be unique and complete.")
        if self._check_party_proportions(db_obj=db_obj, parties_in=parties_in):
            # Not an offer
            raise ValueError("Legitimate offer required.")
        for party_in in parties_in:
            # Force revoke contract approval
            party_in.isApproved = False
            party_in.publicationApproved = False
            crud_party.update(obj_in=party_in)
        if get_raw:
            return db_obj
        return self.get_relationships(db_obj)

    @db.write_transaction
    def approve_or_revoke(self, *, db_obj: Contract, get_raw: bool = False) -> Contract:
        # Can be used to both approve or revoke party contractual updates
        if WorkStateType(db_obj.work.single().state) in [WorkStateType.WITHDRAWN, WorkStateType.SUSPENDED]:
            raise ValueError(f"This contract applies to a work that is currently {db_obj.work.single().state}.")
        contract_in = crud_party.get_relationships(db_objs=db_obj)
        contract_in = ContractUpdate(**ContractInDB.from_orm(contract_in).dict())
        contract_in.isApproved = self.validate_contract(db_obj=db_obj)
        contract_in.publicationApproved = self.validate_publication(db_obj=db_obj)
        contract_in_data = contract_in.as_neo_dict
        Contract.create_or_update(contract_in_data)
        return self._response(db_objs=db_obj, get_raw=get_raw)


contract = CRUDContract(Contract)
