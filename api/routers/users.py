from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.deps import get_db
from schemas.models import User

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@users_router.post("/", response_model=User)
async def create_user(new_user: User, db: AsyncSession = Depends(get_db)):
    # Need to save user to the database here
    return new_user

@users_router.get("/{telegram_id}")
def get_full_user_information_by_telegram_id(telegram_id: int):
    # Need to get user from the database here
    return "Full user information"