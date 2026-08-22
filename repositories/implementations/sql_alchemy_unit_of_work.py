from sqlalchemy.ext.asyncio import AsyncSession


from repositories.implementations.sql_alchemy_item_repo import SqlAlchemieItemsRepository
from repositories.implementations.sql_alchemy_repo import SqlAlchemyRepository
from repositories.implementations.sql_alchemy_user_repo import SqlAlchemieUserRepository
from repositories.unit_of_work import IUnitOfWork

from database.models.user import User
from database.models.category import Category

class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session
        # Special implementation with new methods for Item
        self.items = SqlAlchemieItemsRepository(self.session)
        self.users = SqlAlchemieUserRepository(self.session)
        # Default
        self.category = SqlAlchemyRepository(self.session, Category)

    async def commit(self):
        await self.session.commit()

