from abc import ABC
from typing import Optional

from repositories.i_repository import IRepository
from database import User

class IUserRepository(IRepository[User], ABC):

    async def get_by_tg_id(self, tg_id: int) -> Optional[User]:
        """Get a user by Telegram ID"""
        pass