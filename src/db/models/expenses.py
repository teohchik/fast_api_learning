from datetime import datetime

from sqlalchemy import Integer, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Expense(Base):
    __tablename__ = 'expenses'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)  # 12345678.90
    description: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")

