from schemas.models import User


async def add_user(db: AsyncSession, new_user: User) -> User:
    # Logic to add user to the database
    return new_user