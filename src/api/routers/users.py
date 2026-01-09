from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import PaginationDep
from src.db.crud.users import add_user_db, update_user_db, get_users_db, get_user_db
from src.db.deps import get_db
from src.schemas.user import UserResponse, UserCreate, UserUpdate

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_db(user_id, db)

@users_router.get("/", response_model=list[UserResponse])
async def get_users(pagination: PaginationDep, db: AsyncSession = Depends(get_db)):
    return await get_users_db(pagination, db)


@users_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(new_user_data: UserCreate = Body(openapi_examples={
    "1": {"summary": "Example User", "value":
        {"telegram_id": 123456789, "username": "example_user", "first_name": "example", "last_name": "example"}}}),
        db: AsyncSession = Depends(get_db)):
    return await add_user_db(new_user_data, db)


@users_router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, update_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await update_user_db(user_id, update_data, db)
