from abc import ABC
from typing import Optional,List

from repositories.i_repository import IRepository
from database import Items

class IItemRepository(IRepository[Items],ABC):

    async def get_all_by_category(self, category_id: int) -> List[Items]:
        pass