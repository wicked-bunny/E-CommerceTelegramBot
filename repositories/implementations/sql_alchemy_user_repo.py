from typing import TypeVar, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import User
from database.models.roles import UserRole
from repositories.i_user_repo import IUserRepository
from repositories.implementations.sql_alchemy_repo import SqlAlchemyRepository


class SqlAlchemieUserRepository(SqlAlchemyRepository[User], IUserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_tg_id(self, tg_id: int) -> Optional[User]:
        tg_id_column = getattr(self.model, "tg_id")

        stmt = select(self.model).where(tg_id_column == tg_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()