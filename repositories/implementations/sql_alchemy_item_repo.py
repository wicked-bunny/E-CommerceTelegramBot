from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.i_item_repo import IItemRepository
from repositories.implementations.sql_alchemy_repo import SqlAlchemyRepository
from database.models.items import Items


class SqlAlchemieItemsRepository(SqlAlchemyRepository[Items], IItemRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Items)

    async def get_all_by_category(self, category_id: int) -> List[Items]:
        category_id2 = getattr(self.model, "category_id")

        stmt = select(self.model).where(category_id2 == category_id)
        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def buy_item(self, item_id: int, quantity: int) -> List[Items]:
            """ Asynchronously processes the purchase of a specified item.

        Retrieves the item by its ID, checks its availability, verifies
        if there is sufficient stock, and decrements the stock quantity
        upon a successful check.

        :param item_id: The unique identifier of the item to purchase.
        :param quantity: The number of units to buy.
        :return: A list containing the updated item object.
        :raises ValueError: If the item is not found or if stock is insufficient.
        """

            id_attr = getattr(self.model, "id")
            stmt = select(self.model).where(id_attr == item_id)

            result = await self.session.execute(stmt)
            item = result.scalars().first()

            if item is None:
                raise ValueError(f"Item with ID {item_id} not found in database.")

            if item.quantity_in_stock < quantity:
                raise ValueError(f"Not enough stock for item {item_id}. Available: {item.quantity_in_stock}")

            item.quantity_in_stock -= quantity

            self.session.add(item)
            return [item]

    async def buy_one_item(self, item_id: int) -> Optional[Items]:
        await self.buy_item(item_id, 1)



