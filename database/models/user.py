from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from database.models import BaseModel
from database.models.roles import UserRole


class User(BaseModel):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    username: Mapped[str | None]
    fullname: Mapped[str]

    role: Mapped[str] = mapped_column(default=UserRole.USER)
