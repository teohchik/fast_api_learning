from typing import Any, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.users import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException, status

from db.repositories.users import UsersRepository
from schemas.user import UserCreate, UserUpdate, UserResponse
from schemas.user import UserResponse


async def get_users_db(db: AsyncSession) -> list[UserResponse]:
    users_response = await UsersRepository(db).get_all()
    return [
        UserResponse.model_validate(user)
        for user in users_response
    ]


async def add_user_db(new_user_data: UserCreate, db: AsyncSession) -> UserResponse:
    try:
        db_user = await UsersRepository(db).add(new_user_data)
        await db.commit()
        print(f"Added new user with ID: {db_user.id}")
    except IntegrityError as exc:
        await db.rollback()
        print("IntegrityError occurred while adding a new user:", exc)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this telegram_id already exists."
        )

    return UserResponse.model_validate(db_user)


async def update_user_db(user_id: int, update_data: UserUpdate, db: AsyncSession):
    try:
        db_user = await UsersRepository(db).edit_by_id(update_data, user_id)
        await db.commit()
    except NoResultFound:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return UserResponse.model_validate(db_user)
