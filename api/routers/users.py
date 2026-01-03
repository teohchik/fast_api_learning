from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.users import add_user_db, update_user_db
from db.deps import get_db
from schemas.user import UserResponse, UserCreate, UserUpdate

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(new_user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await add_user_db(new_user_data, db)

@users_router.patch("/{telegram_id}", response_model=UserResponse)
async def update_user(telegram_id: int, update_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await update_user_db(telegram_id, update_data, db)
