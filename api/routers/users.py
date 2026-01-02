from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.users import add_user
from db.deps import get_db
from schemas.user import UserResponse, UserCreate

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(new_user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await add_user(new_user_data, db)

@users_router.get("/{telegram_id}")
def get_full_user_information_by_telegram_id(telegram_id: int):
    # Need to get user from the database here
    return "Full user information"