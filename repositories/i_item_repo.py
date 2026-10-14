from abc import ABC
from typing import Optional,List

from repositories.i_repository import IRepository
from database import Items

class IItemRepository(IRepository[Items],ABC):

    async def get_all_by_category(self, category_id: int) -> List[Items]:
        pass
    async def buy_item(self, item_id: int, quantity: int ) -> Optional[Items]:
        pass
    async def buy_one_item(self, item_id: int) -> Optional[Items]:
        await self.buy_item(item_id, 1)