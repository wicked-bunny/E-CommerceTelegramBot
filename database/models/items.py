from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from database.models import BaseModel


class Items(BaseModel):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    file_id: Mapped[str]
    file_unic_id: Mapped[str]
    description: Mapped[str]
    price: Mapped[int] # 1$ = 100
    quantity_in_stock:Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))       # item to category