from .crud_user import user
from .crud_token import token
from .crud_spaces import spaces
from .crud_files import files
from .crud_epub import epub
from .crud_cover import cover
from .crud_creator import creator
from .crud_subject import subject
from .crud_contributor import contributor
from .crud_work_metadata import work_metadata
from .crud_work import work
from .crud_party import party
from .crud_contract import contract
from .crud_history import history
from .crud_search import search
from .crud_bookmark import bookmark


# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
