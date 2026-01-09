from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ExpenseCreate(BaseModel):
    category_id: int = Field(gt=0)
    amount: float = Field(gt=0, le=1_000_000)
    description: str = Field(min_length=1, max_length=500)

class ExpenseUpdate(BaseModel):
    amount: float | None = Field(default=None, gt=0, le=1_000_000)
    description: str | None = Field(default=None, min_length=1, max_length=500)

class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    category_id: int
    amount: float
    description: str
    created_at: datetime