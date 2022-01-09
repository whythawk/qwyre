from typing import List, Union
from neomodel import db, Q, CardinalityViolation, MultipleNodesReturned

from app.crud.neo_base import NeoCRUDBase
from app.models import Bookmark, Creator, Work
from app.schemas import BookmarkCreate, BookmarkUpdate


class CRUDBookmark(NeoCRUDBase[Bookmark, BookmarkCreate, BookmarkUpdate]):
    @db.write_transaction
    def add_reader(self, *, db_obj: Bookmark, creator_obj: Creator) -> Bookmark:
        try:
            old_creator_obj = db_obj.reader.single()
            db_obj.reader.reconnect(old_node=old_creator_obj, new_node=creator_obj)
        except CardinalityViolation:
            db_obj.reader.connect(creator_obj)
        return db_obj

    @db.write_transaction
    def add_reading(self, *, db_obj: Bookmark, work_obj: Work) -> Bookmark:
        try:
            old_work_obj = db_obj.reading.single()
            db_obj.contract.reconnect(old_node=old_work_obj, new_node=work_obj)
        except CardinalityViolation:
            db_obj.reading.connect(work_obj)
        return db_obj

    def dogear(self, *, obj_in: BookmarkCreate, creator_obj: Creator, work_obj: Work) -> BookmarkUpdate:
        bookmark_obj = self.create(obj_in=obj_in, get_raw=True)
        bookmark_obj = self.add_reader(db_obj=bookmark_obj, creator_obj=creator_obj)
        bookmark_obj = self.add_reading(db_obj=bookmark_obj, work_obj=work_obj)
        return BookmarkUpdate.from_orm(bookmark_obj)

    def get_from_creator(self, *, creator_obj: Creator, work_obj: Work) -> BookmarkUpdate:
        db_objs = creator_obj.reading.all()
        bookmark_in = None
        for bookmark_obj in db_objs:
            try:
                reading_obj = bookmark_obj.reading.single()
                if reading_obj.identifier == work_obj.identifier:
                    bookmark_in = BookmarkUpdate.from_orm(bookmark_obj)
                    break
            except CardinalityViolation:
                continue
        return bookmark_in

    @db.write_transaction
    def toggle_ownership(self, *, obj_in: BookmarkUpdate) -> BookmarkUpdate:
        # neo_dict wrecks booleans ...
        obj_in_data = obj_in.as_neo_dict
        obj_in_data["isOwned"] = True
        db_obj = self.model.create_or_update(obj_in_data)  # type: ignore
        return BookmarkUpdate(**obj_in_data)


bookmark = CRUDBookmark(Bookmark)
