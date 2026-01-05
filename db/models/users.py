from sqlalchemy import Integer, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(length=255))
    first_name: Mapped[str] = mapped_column(String(length=255))
    last_name: Mapped[str | None] = mapped_column(String(length=255))
    categories = relationship("Category", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
