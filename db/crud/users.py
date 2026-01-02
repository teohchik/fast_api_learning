from sqlalchemy.ext.asyncio import AsyncSession

from db.models.users import User
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from schemas.user import UserCreate
from schemas.user import UserResponse


async def add_user(new_user_data: UserCreate, db: AsyncSession) -> UserResponse:
    try:
        db_user = User(**new_user_data.model_dump())
        db.add(db_user)
        await db.commit()
        print(f"Added new user with ID: {db_user.id}")
    except IntegrityError as exc:
        await db.rollback()
        print("IntegrityError occurred while adding a new user:", exc)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач з таким Telegram ID вже існує"
        )

    return UserResponse.model_validate(db_user)
