from fastapi import APIRouter, status, Depends

from src.api.deps import PaginationDep, verify_bot_api_key
from src.db.crud.users import add_user_db, update_user_db, get_users_db, get_user_db
from src.db.deps import DBDep
from src.schemas.user import UserResponse, UserCreate, UserUpdate

users_router = APIRouter(
    prefix="/users", dependencies=[Depends(verify_bot_api_key)], tags=["Users"]
)


@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: DBDep):
    return await get_user_db(user_id, db)


@users_router.get("/", response_model=list[UserResponse])
async def get_users(pagination: PaginationDep, db: DBDep):
    return await get_users_db(pagination, db)


@users_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(new_user_data: UserCreate, db: DBDep):
    return await add_user_db(new_user_data, db)


@users_router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, update_data: UserUpdate, db: DBDep):
    return await update_user_db(user_id, update_data, db)
