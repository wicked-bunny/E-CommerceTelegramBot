from database.models.category import Category
from repositories.i_item_repo import IItemRepository
from repositories.i_repository import IRepository
from repositories.i_user_repo import IUserRepository
from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
    # Generic Type
    users: IUserRepository
    category: IRepository[Category]
    items: IItemRepository

    @abstractmethod
    async def commit(self):
        pass

    async def __aenter__(self): return self

    async def __aexit__(self, exc_type, exc_val, exc_tb): pass