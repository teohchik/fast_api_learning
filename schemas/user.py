from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    telegram_id: str = Field(min_length=1, max_length=50)
    username: str = Field(min_length=1, max_length=100)
    first_name: str = Field(min_length=1, max_length=100)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    username: str
    first_name: str