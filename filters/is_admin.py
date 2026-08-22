from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.models.roles import UserRole
from repositories.unit_of_work import IUnitOfWork


class IsAdmin(BaseFilter):
    async def __call__(
            self,
            message: Message,
            unit_of_work: IUnitOfWork
    ) -> bool:
        user = await unit_of_work.users.get_by_tg_id(message.from_user.id)

        if not user:
            return False

        return user.role in (UserRole.ADMIN, UserRole.SUPER_ADMIN)
