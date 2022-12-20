from typing import List, Union, Optional
from neomodel import db, Q
from uuid import UUID

from neomodel.exceptions import CardinalityViolation

from app.crud.neo_base import NeoCRUDBase
from app.crud.crud_party import party as crud_party
from app.models import Party, Contract, Creator, User, Work, Anthology, Series
from app.schemas import (
    ContractCreate,
    ContractUpdate,
    ContractInDB,
    PartyCreatorCreate,
    PartyCreate,
    PartyUpdate,
    PartyInDB,
)
from app.schema_types import WorkStateType, ContributorRoleType
from app.crud import contributor as crud_contributor


class CRUDContract(NeoCRUDBase[Contract, ContractCreate, ContractUpdate]):
    def get_work(self, *, db_obj: Contract) -> Optional[Work]:
        try:
            return db_obj.work.single()
        except CardinalityViolation:
            return None

    def has_appropriate_rights(self, *, creator_obj: Creator, contract_obj: Contract, user_obj: User,) -> bool:
        if user_obj.is_superuser or user_obj.is_moderator:
            return True
        party_identifiers = []
        for party in contract_obj.parties.all():
            try:
                party_identifiers.append(party.creator.single().identifier)
            except CardinalityViolation:
                pass
        if creator_obj.identifier in party_identifiers:
            return True
        return False

    def has_elevated_rights(self, *, creator_obj: Creator, contract_obj: Contract, user_obj: User,) -> bool:
        if not self.has_appropriate_rights(creator_obj=creator_obj, contract_obj=contract_obj, user_obj=user_obj):
            return False
        # And then is only about being a creator or super-user of the work
        work_obj = contract_obj.work.single()
        return crud_contributor.has_appropriate_rights(
            creator_obj=creator_obj,
            work_obj=work_obj,
            user_obj=user_obj,
            roles=[ContributorRoleType.AUTHOR, ContributorRoleType.MODERATOR,],
        )

    def can_assign_parties(self, *, db_obj: Contract) -> bool:
        # The contract must not be signed, and there must be a party where the creator is null.
        if db_obj.isApproved:
            return False
        try:
            # Will break if any are not assigned
            [party.creator.single() for party in db_obj.parties.all()]
        except CardinalityViolation:
            return True
        return False

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
        db_obj: Optional[Contract] = None,
        parties_in: Union[List[PartyCreatorCreate], PartyCreatorCreate, List[PartyUpdate], PartyUpdate],
    ) -> bool:
        if not isinstance(parties_in, list):
            parties_in = [parties_in]
        if not any(party.proportion >= 1 or party.proportion >= 99 for party in parties_in):
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

    def _update_parties(self, *, parties_in: List[PartyUpdate]) -> None:
        for party_in in parties_in:
            creator = None
            if party_in.creator:
                creator = Creator.nodes.get_or_none(identifier=self._hexify(party_in.creator))
                if not creator:
                    raise ValueError(f"Creator {party_in.creator} does not exist.")
            party_in_data = party_in.as_neo_dict
            party_obj = Party.create_or_update(party_in_data)[0]
            try:
                if (
                    party_obj.creator.single()
                    and creator
                    and creator.identifier != party_obj.creator.single().identifier
                ):
                    party_obj.creator.single().contracts.disconnect(party_obj)
                    creator.contracts.connect(party_obj)
            except CardinalityViolation:
                if creator:
                    creator.contracts.connect(party_obj)

    @db.write_transaction
    def create(
        self, *, obj_in: ContractCreate, connect_obj: Union[Work, Series, Anthology], get_raw: bool = False,
    ) -> Contract:
        if not self._check_parties_unique(parties_in=obj_in.parties):
            # Not unique
            raise ValueError("Parties to the contract must be unique.")
        if not self._check_party_proportions(parties_in=obj_in.parties):
            # Not an offer
            raise ValueError("Legitimate offer required.")
        # Create the contract and assign the parties to the contract
        obj_in_data = obj_in.as_neo_dict
        obj_in_data.pop("parties")
        db_obj = self.model.create_or_update(obj_in_data)[0]
        connect_obj.contract.connect(db_obj)
        db_obj = self._add_parties(db_obj=db_obj, parties_in=obj_in.parties)
        return self._response(db_objs=db_obj, get_raw=get_raw)

    @db.write_transaction
    def update(self, *, obj_in: ContractUpdate, get_raw: bool = False) -> Contract:
        if not self._check_parties_unique(parties_in=obj_in.parties):
            # Not unique
            raise ValueError("Parties to the contract must be unique.")
        if not self._check_party_proportions(parties_in=obj_in.parties):
            # Not an offer
            raise ValueError("Legitimate offer required.")
        obj_in_data = obj_in.as_neo_dict
        obj_in_data.pop("parties")
        # type: ignore
        self._update_parties(parties_in=obj_in.parties)
        db_obj = self.model.create_or_update(obj_in_data)[0]
        return self._response(db_objs=db_obj, get_raw=get_raw)

    def validate_contract(self, *, db_obj: Contract) -> bool:
        return all(party.isApproved for party in db_obj.parties.all())

    def validate_publication(self, *, db_obj: Contract) -> bool:
        return all(party.publicationApproved for party in db_obj.parties.all())

    @db.write_transaction
    def reset_on_change(self, *, db_obj: Contract, get_raw: bool = False) -> Contract:
        for party in db_obj.parties:
            party_in = crud_party.get_relationships(db_objs=party)
            party_in = PartyUpdate.from_orm(party_in)
            party_in_data = party_in.as_neo_dict
            party_in_data["publicationApproved"] = False
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

    def get_party(self, *, db_obj: Contract, creator_id: UUID) -> Optional[Party]:
        creator_id = self._hexify(creator_id)
        for party in db_obj.parties.all():
            try:
                if party.creator.single().identifier == creator_id:
                    return party
            except CardinalityViolation:
                pass

    @db.write_transaction
    def remove_party(self, *, db_obj: Party, get_raw: bool = False,) -> Optional[Party]:
        try:
            creator_obj = db_obj.creator.single()
        except CardinalityViolation:
            return None
        creator_obj.contracts.disconnect(db_obj)
        return self._response(db_objs=db_obj, get_raw=get_raw)

    @db.write_transaction
    def add_party(self, *, db_obj: Contract, creator_obj: Creator, get_raw: bool = False,) -> Optional[Party]:
        for party_obj in db_obj.parties.all():
            try:
                party_obj.creator.single()
            except CardinalityViolation:
                creator_obj.contracts.connect(party_obj)
                break
        return self._response(db_objs=db_obj, get_raw=get_raw)

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
    def toggle_party_contract_approval(
        self, *, contract_obj: Contract, party_obj: Party, get_raw: bool = False
    ) -> Contract:
        # Need to update party, and the contract itself
        if contract_obj.isApproved:
            raise ValueError("Contract has already been signed by all parties.")
        party_in = PartyUpdate.from_orm(party_obj)
        party_in_data = party_in.as_neo_dict
        party_in_data["isApproved"] = not party_obj.isApproved
        party_obj = Party.create_or_update(party_in_data)[0]
        if self.validate_contract(db_obj=contract_obj):
            contract_in = ContractUpdate.from_orm(contract_obj)
            contract_in_data = contract_in.as_neo_dict
            contract_in_data["isApproved"] = True
            contract_obj = Contract.create_or_update(contract_in_data)
        return self._response(db_objs=contract_obj, get_raw=get_raw)

    @db.write_transaction
    def toggle_party_contract_publication(
        self, *, contract_obj: Contract, party_obj: Party, get_raw: bool = False
    ) -> Contract:
        # Need to update party, and the contract itself
        if not contract_obj.isApproved:
            raise ValueError("Contract must be signed by all parties.")
        if contract_obj.publicationApproved:
            raise ValueError("Publication has been approved by all parties.")
        party_in = PartyUpdate.from_orm(party_obj)
        party_in_data = party_in.as_neo_dict
        party_in_data["publicationApproved"] = not party_obj.publicationApproved
        party_obj = Party.create_or_update(party_in_data)[0]
        if self.validate_publication(db_obj=contract_obj):
            contract_in = ContractUpdate.from_orm(contract_obj)
            contract_in_data = contract_in.as_neo_dict
            contract_in_data["publicationApproved"] = True
            contract_obj = Contract.create_or_update(contract_in_data)
        return self._response(db_objs=contract_obj, get_raw=get_raw)

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

    @db.read_transaction
    def get_multi_as_party(
        self, *, creator_obj: Creator, skip: int = 0, limit: int = 100, get_raw: bool = False
    ) -> List[Contract]:
        # This excludes works the creator actually created, rather than contributes to
        work_identifiers = []
        for metadata in creator_obj.works.all():
            try:
                work_identifiers.append(metadata.work.single().contract.single().identifier)
            except CardinalityViolation:
                continue
        contract_objs = []
        for party_obj in creator_obj.contracts.all():
            try:
                if party_obj.contract.single().identifier not in work_identifiers:
                    contract_objs.append(party_obj.contract.single())
            except CardinalityViolation:
                continue
        contract_objs = contract_objs[skip : limit + skip]
        return self._response(db_objs=contract_objs, get_raw=get_raw, get_first=False)

    @db.read_transaction
    def get_multi_by_offered(self, *, skip: int = 0, limit: int = 100, get_raw: bool = False) -> List[Contract]:
        work_objs = Work.nodes.filter(Q(state=WorkStateType.OFFERED.value.upper()))[skip : limit + skip]
        db_objs = [work.contract.single() for work in work_objs]
        return self._response(db_objs=db_objs, get_raw=get_raw, get_first=False)


contract = CRUDContract(Contract)
