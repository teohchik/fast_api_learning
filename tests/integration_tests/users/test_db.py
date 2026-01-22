from src.schemas.user import UserCreate


async def test_add_user(db):
    user_add = UserCreate(telegram_id=543153452345, username="test_user", first_name="Test User", last_name="Test User")
    new_user_data = await db.users.add(user_add)
    await db.commit()
    print(f"{new_user_data=}")
