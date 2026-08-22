from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from repositories.implementations.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork


class DatabaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_maker) -> None:
        self.session_maker = session_maker

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
        ) -> Any:
        async with self.session_maker() as session:
            # Create an exemplar of Unit Of Work
            unit_of_work = SqlAlchemyUnitOfWork(session=session)
            # We store it in the "unit_of_work" key in the data
            data["unit_of_work"] = unit_of_work

            return await handler(event, data)