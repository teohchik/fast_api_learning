from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    telegram_id: int
    username: Optional[str] = Field(None, max_length=255)
    first_name: str = Field(min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    username: Optional[str] = Field(None, max_length=255)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
