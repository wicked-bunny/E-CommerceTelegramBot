from abc import ABC, abstractmethod
from database.models.user import User
from database.models.category import Category
from database.models.items import Items
from repositories.i_item_repo import IItemRepository
from repositories.i_repository import IRepository
from repositories.i_user_repo import IUserRepository


class IUnitOfWork(ABC):
    # Generic Type
    users: IUserRepository
    category: IRepository[Category]
    items: IItemRepository

    # If you want a neu method for your (exemple) user, you want to create a new Interface special for user
    # Ex: users: IUserRepository
    @abstractmethod
    async def commit(self):
        pass