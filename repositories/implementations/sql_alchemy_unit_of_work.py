from sqlalchemy.ext.asyncio import AsyncSession
from database import session_maker  # Import your global session factory

from repositories.implementations.sql_alchemy_item_repo import SqlAlchemieItemsRepository
from repositories.implementations.sql_alchemy_repo import SqlAlchemyRepository
from repositories.implementations.sql_alchemy_user_repo import SqlAlchemieUserRepository
from repositories.unit_of_work import IUnitOfWork

from database.models.category import Category


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession = None):
        """Initializes the Unit of Work and sets up repositories with the active session."""
        # If session is provided (from middleware), use it. Otherwise, create a new one.
        self.session = session if session else session_maker()

        # Track if UoW owns the session lifecycle to close it later
        self._owns_session = session is None

        self.items = SqlAlchemieItemsRepository(self.session)
        self.users = SqlAlchemieUserRepository(self.session)
        self.category = SqlAlchemyRepository(self.session, Category)

    async def __aenter__(self):
        """Activates the asynchronous context manager boundary and returns the UoW instance."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Automatically manages database connection lifecycles and handles potential failures."""
        if exc_type:
            # If an unhandled exception occurs inside the 'async with' block, roll back changes safely
            await self.session.rollback()

        # Securely close the explicit database session connection thread
        if hasattr(self, "_owns_session") and self._owns_session:
            await self.session.close()
        else:
            # Fallback backup execution to ensure no dangling connections remain open
            await self.session.close()

    async def commit(self):
        """Persists all current session transaction updates to the database store."""
        await self.session.commit()

    async def rollback(self):
        """Safely rolls back the current database session transaction."""
        await self.session.rollback()
