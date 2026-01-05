from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    user_id: int = Field(gt=0)

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    user_id: int
    created_at: datetime