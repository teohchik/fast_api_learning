from datetime import datetime

from pydantic import BaseModel, Field


class SalaryCreate(BaseModel):
    user_id: int = Field(gt=0)
    amount: float = Field(gt=0, le=1_000_000)
    description: str | None = Field(default=None, min_length=1, max_length=500)
    created_at: datetime | None = Field(default=datetime.now())


class SalaryUpdate(BaseModel):
    amount: float | None = Field(default=None, gt=0, le=1_000_000)
    description: str | None = Field(default=None, min_length=1, max_length=500)


class SalaryResponse(BaseModel):
    # model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    amount: float
    description: str | None
    created_at: datetime
