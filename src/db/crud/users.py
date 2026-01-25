from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.db.db_manager import DBManager
from src.db.repositories.users import UsersRepository
from src.schemas.user import UserCreate, UserUpdate
from src.schemas.user import UserResponse


async def get_user_db(user_id, db: DBManager) -> UserResponse:
    user_response = await db.users.get_one_or_none(id=user_id)
    if not user_response:
        raise HTTPException(status_code=404, detail="User not found")
    return user_response


async def get_users_db(pagination, db: DBManager) -> list[UserResponse]:
    users_response = await db.users.get_by_filters(
        pagination=pagination, order_by=UsersRepository.model.id
    )
    return users_response


async def add_user_db(new_user_data: UserCreate, db: DBManager) -> UserResponse:
    try:
        db_user = await db.users.add(new_user_data)
        await db.commit()
        print(f"Added new user with ID: {db_user.id}")
    except IntegrityError as exc:
        print("IntegrityError occurred while adding a new user:", exc)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this telegram_id already exists.",
        )

    return db_user


async def update_user_db(user_id: int, update_data: UserUpdate, db: DBManager) -> UserResponse:
    try:
        db_user = await db.users.edit_by_id(update_data, user_id)
        await db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user
