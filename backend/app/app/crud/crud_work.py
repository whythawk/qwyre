from typing import List, Union, Optional
from neomodel import db, Q, CardinalityViolation
from neomodel.util import change_neo4j_password
from uuid import UUID
import random

from app.core.config import settings
from app.crud.neo_base import NeoCRUDBase
from app.models import Work, WorkMetadata, Contract, StateHistory, Creator
from app.schemas import WorkCreate, WorkUpdate, WorkInDB, RevenueShare, StreamFirst, StreamSecond
from app.schema_types import WorkStateType
from app.schemas.bookmark import BookmarkUpdate


class CRUDWork(NeoCRUDBase[Work, WorkCreate, WorkUpdate]):
    def has_contract(self, *, db_obj: Work):
        try:
            db_obj.contract.single()
            return True
        except CardinalityViolation:
            return False

    def is_work_creator(self, *, db_obj: Work, creator_obj: Creator) -> bool:
        creator_identifiers = []
        for creator in db_obj.metadata.single().creator.all():
            creator_identifiers.append(creator.identifier)
        if creator_obj.identifier in creator_identifiers:
            return True
        return False

    def has_state(self, *, db_obj: Work, state: WorkStateType) -> bool:
        if WorkStateType(db_obj.state) == state:
            return True
        return False

    def validate_editing_permitted(self, *, db_obj: Work):
        if not self.has_contract(db_obj=db_obj):
            return True
        if (
            WorkStateType(db_obj.state)
            not in [WorkStateType.SUSPENDED, WorkStateType.PUBLISHED, WorkStateType.WITHDRAWN]
            or not db_obj.contract.single().publicationApproved
        ):
            return True
        return False

    def validate_state_change_by_creator(self, *, db_obj: Work, change_state: WorkStateType):
        # Used only to offer a contract, or publish a work
        if not self.has_contract(db_obj=db_obj):
            return False
        if change_state == WorkStateType.OFFERED and WorkStateType(db_obj.state) in [
            WorkStateType.UPDATED,
            WorkStateType.SUBMITTED,
        ]:
            return True
        if change_state == WorkStateType.PUBLISHED and db_obj.contract.single().publicationApproved:
            return True
        return False

    def get_contract(self, *, db_obj: Work, get_raw: bool = False):
        try:
            db_objs = db_obj.contract.single()
            return self._response(db_objs=db_objs, get_raw=get_raw)
        except CardinalityViolation:
            # A work may not yet have initialised a contract (e.g. just created)
            return None

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
    def get_from_metadata(self, *, id: UUID, get_raw: bool = False) -> Optional[Work]:
        id = self._hexify(id)
        metadata_obj = WorkMetadata.nodes.get_or_none(identifier=id)
        try:
            db_obj = metadata_obj.work.single()
        except CardinalityViolation:
            return None
        return self._response(db_objs=db_obj, get_raw=get_raw)

    @db.read_transaction
    def get_multi_by_state(self, *, state: WorkStateType, skip: int = 0, limit: int = 100) -> List[Work]:
        db_objs = self.model.nodes.filter(Q(state=state.value.upper()))[skip : limit + skip]
        return self.get_relationships(db_objs)

    @db.read_transaction
    def get_multi_published_by_creator(self, *, skip: int = 0, limit: int = 100) -> List[Work]:
        db_objs = self.model.nodes.filter(Q(state=WorkStateType.PUBLISHED.value.upper()))[skip : limit + skip]
        return self.get_relationships(db_objs)

    @db.read_transaction
    def get_multi_published_by_subject(self, *, skip: int = 0, limit: int = 100) -> List[Work]:
        db_objs = self.model.nodes.filter(Q(state=WorkStateType.PUBLISHED.value.upper()))[skip : limit + skip]
        return self.get_relationships(db_objs)

    @db.write_transaction
    def update_state(self, *, db_obj: Work, history_obj: StateHistory, get_raw: bool = False) -> Work:
        db_obj.history.connect(history_obj)
        work_in = WorkUpdate.from_orm(db_obj)
        work_in.state = history_obj.state
        work_in_data = work_in.as_neo_dict
        db_obj = Work.create_or_update(work_in_data)
        return self._response(db_objs=db_obj, get_raw=get_raw)

    @db.write_transaction
    def withdraw_or_suspend(self, *, db_obj: Work, history_obj: StateHistory, get_raw: bool = False) -> Work:
        if WorkStateType(history_obj.state) not in [WorkStateType.WITHDRAWN, WorkStateType.SUSPENDED]:
            raise ValueError(f"This function only applies for the withdrawal or suspension of a work.")
        return self.update_state(db_objs=db_obj, history_obj=history_obj, get_raw=get_raw)

    @db.read_transaction
    def get_stream_first(self, *, id: UUID) -> Optional[StreamFirst]:
        id = self._hexify(id)
        db_obj = self.model.nodes.get_or_none(identifier=id)
        if not db_obj:
            return db_obj
        stream_in = StreamFirst.from_orm(db_obj)
        page = 0
        position = settings.STREAM_FIRST
        if stream_in.start_page:
            # There is a start page
            page = stream_in.start_page
            stream = [stream_in.stream[:page]]
        # Loop and keep a tally of the words still to be added
        while True:
            if len(stream_in.stream[page]) < position:
                stream.append(stream_in.stream[page])
                position -= len(stream_in.stream[page])
                page += 1
            else:
                stream.append(stream_in.stream[page][:position])
                break
        stream_in.stream = stream
        stream_in.page = page
        stream_in.position = position
        return stream_in

    def get_revenue_share(self, *, db_obj: Work) -> List[RevenueShare]:
        revenue_parties = db_obj.contract.single().parties.all()
        revenue_share = [RevenueShare(**{"proportion": settings.STREAM_SHARE / 100, "wallet": settings.STREAM_WALLET,})]
        multiplier = (100 - settings.STREAM_SHARE) / 100
        for party in revenue_parties:
            revenue_share.append(
                RevenueShare(
                    **{"proportion": multiplier * party.proportion / 100, "wallet": party.creator.single().wallet,}
                )
            )
        return revenue_share

    def get_revenue_choice(self, *, parties_in: List[RevenueShare]) -> str:
        revenue_choice = random.choices(
            population=[party.wallet for party in parties_in], weights=[party.proportion for party in parties_in], k=1
        )
        if not revenue_choice or not revenue_choice[0]:
            return settings.STREAM_WALLET
        return revenue_choice[0]

    def get_stream_first(self, *, db_obj: Work, bookmark_in: Optional[BookmarkUpdate] = None) -> Optional[StreamFirst]:
        stream_in = StreamFirst.from_orm(db_obj)
        last_page = len(stream_in.stream) - 1
        last_position = len(stream_in.stream[last_page]) - 1
        longest_position = max(len(p) for p in stream_in.stream)
        if bookmark_in and (
            bookmark_in.isOwned
            or (
                bookmark_in.page
                and bookmark_in.position
                and bookmark_in.page == last_page
                and bookmark_in.position == last_position
            )
        ):
            # return the full text
            stream_in.page = last_page
            stream_in.position = last_position
            return stream_in
        page = 0
        position = 0
        if stream_in.start_page:
            page = stream_in.start_page
        stream = stream_in.stream[:page]
        if bookmark_in and (
            bookmark_in.page
            and bookmark_in.position
            and bookmark_in.page < last_page
            and bookmark_in.position <= longest_position
        ):
            # Either it's already owned, or it is partially streamed
            first = sum([len(p) for p in db_obj.stream[page : bookmark_in.page]]) + bookmark_in.position
        else:
            first = settings.STREAM_FIRST
        # Loop and keep a tally of the words still to be added
        try:
            while True:
                words = db_obj.stream[page][position : position + first]
                stream.append(words)
                if len(words) < first:
                    first -= len(words)
                    position = 0
                    page += 1
                else:
                    position += first
                    break
        except IndexError:
            pass
        if page > last_page:
            page = last_page
            position = last_position
        stream_in.stream = stream
        stream_in.page = page
        stream_in.position = position
        return stream_in

    def get_stream_second(self, *, db_obj: Work, page: int, position: int) -> Optional[StreamSecond]:
        stream = []
        second = settings.STREAM_PER_SECOND
        # Loop and keep a tally of the words still to be added
        try:
            while True:
                words = db_obj.stream[page][position : position + second]
                stream.append(words)
                if len(words) < second:
                    second -= len(words)
                    position = 0
                    page += 1
                else:
                    position += second
                    break
        except IndexError:
            pass
        stream_in = StreamSecond(
            **{"identifier": UUID(db_obj.identifier), "stream": stream, "page": page, "position": position,}
        )
        return stream_in

    @db.write_transaction
    def remove(self, *, id: UUID) -> bool:
        id = self._hexify(id)
        obj = self.model.nodes.get(identifier=id)
        try:
            metadata_obj = obj.metadata.single()
            metadata_obj.delete()
        except CardinalityViolation:
            pass
        try:
            contract_obj = obj.contract.single()
            contract_obj.delete()
        except CardinalityViolation:
            pass
        try:
            history_objs = obj.history.all()
            for h in history_objs:
                h.delete()
        except CardinalityViolation:
            pass
        obj = obj.delete()
        return obj


work = CRUDWork(Work)
