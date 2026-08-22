from typing import TypeVar, Type, Optional, List

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import BaseModel
from repositories.i_repository import IRepository

T = TypeVar('T', bound=BaseModel)


class SqlAlchemyRepository(IRepository[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get_all(self) -> List[T]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def get_by_id(self, obj_id: int) -> Optional[T]:

        id_column = getattr(self.model,"id")

        stmt = select(self.model).where(id_column == obj_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


    async def update_by_id(self, obj_id: int, data: dict) -> bool:
        id_column = getattr(self.model, "id")

        stmt = (
            update(self.model)
            .where(id_column == obj_id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        result = await self.session.execute(stmt)

        # rowcount returns the number of modified rows
        return result.rowcount > 0

    async def add(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def delete(self, obj_id: int) -> bool:
        id_column = getattr(self.model, "id")
        stmt = (
            delete(self.model)
            .where(id_column == obj_id)
            .execution_options(synchronize_session="fetch")
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0