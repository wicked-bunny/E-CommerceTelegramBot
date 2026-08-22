from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.i_item_repo import IItemRepository
from repositories.implementations.sql_alchemy_repo import SqlAlchemyRepository
from database.models.items import Items

from repositories.i_repository import IRepository

class SqlAlchemieItemsRepository(SqlAlchemyRepository[Items], IItemRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Items)

    async def get_all_by_category(self, category_id: int) -> List[Items]:
        category_id2 = getattr(self.model, "category_id")

        stmt = select(self.model).where(category_id2 == category_id)
        result = await self.session.execute(stmt)

        return list(result.scalars().all())



