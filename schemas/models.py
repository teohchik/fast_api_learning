from pydantic import BaseModel

class User(BaseModel):
    id: int
    telegram_id: int
    username: str | None
    first_name: str | None

class Category(BaseModel):
    id: int
    title: str
    user_id: User
