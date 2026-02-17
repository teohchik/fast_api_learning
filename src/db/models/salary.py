from datetime import datetime

from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Salary(Base):
    __tablename__ = "salaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    user = relationship("User", back_populates="salaries")
