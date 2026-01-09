from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    telegram_id: int = Field(gt=0)
    username: str | None = Field(None, max_length=255)
    first_name: str = Field(min_length=1, max_length=255)
    last_name: str | None = Field(None, max_length=255)


class UserUpdate(BaseModel):
    username: str | None = Field(None, max_length=255)
    first_name: str | None = Field(None, min_length=1, max_length=255)
    last_name: str | None = Field(None, max_length=255)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    username: str | None = None
    first_name: str
    last_name: str | None = None
