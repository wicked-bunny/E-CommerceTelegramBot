from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')
class IRepository(ABC, Generic[T]):
    """Source Interface"""

    @abstractmethod
    async def get_all(self) -> List[T]:
        """Returns all records from the table by its ID"""
        pass
    @abstractmethod
    async def get_by_id(self, obj_id: int)-> Optional[T]:
        """Returns one record from table by its ID"""
        pass
    @abstractmethod
    async def update_by_id(self, obj_id: int, data: dict) -> bool:
        """Updates one record from table by its ID"""
        pass
    @abstractmethod
    async def add(self, entity: T) -> T:
        """adds a new object"""
        pass
    @abstractmethod
    async def delete(self, obj_id: int) -> bool:
        """Deletes a record from a table by its ID"""
        pass
