from datetime import datetime

from sqlalchemy import Integer, String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func

from src.db.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(length=255))
    first_name: Mapped[str] = mapped_column(String(length=255))
    last_name: Mapped[str | None] = mapped_column(String(length=255))
    currency: Mapped[str] = mapped_column(String(length=10), default="€", server_default="€")
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    categories = relationship("Category", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
