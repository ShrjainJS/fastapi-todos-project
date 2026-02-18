from database.database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str | None] = mapped_column()

class Todos(Base):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column()
    priority: Mapped[int] = mapped_column()
    complete: Mapped[bool] = mapped_column(default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


