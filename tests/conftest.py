import json

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.config.settings import settings
from src.db.base import Base
from src.db.db_manager import DBManager
from src.db.session import AsyncSessionLocalNullPool, engine

from src.main import app
from src.schemas.category import CategoryCreate
from src.schemas.expense import ExpenseCreate
from src.schemas.user import UserCreate


@pytest_asyncio.fixture(scope="function")
async def db():
    async with DBManager(session_factory=AsyncSessionLocalNullPool) as db:
        yield db


@pytest.fixture(autouse=True, scope="session")
def check_test_mode():
    assert settings.MODE == "TEST", "Tests must be run in TEST mode!"


@pytest.fixture(autouse=True, scope="session")
async def setup_database(check_test_mode):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/users.json", encoding="utf-8") as file_users:
        users = json.load(file_users)
    with open("tests/categories.json", encoding="utf-8") as file_categories:
        categories = json.load(file_categories)
    with open("tests/expenses.json", encoding="utf-8") as file_expenses:
        expenses = json.load(file_expenses)

    users = [UserCreate.model_validate(user_) for user_ in users]
    categories = [CategoryCreate.model_validate(category_) for category_ in categories]
    expenses = [ExpenseCreate.model_validate(expense_) for expense_ in expenses]

    async with DBManager(session_factory=AsyncSessionLocalNullPool) as db_:
        await db_.users.add_bulk(users)
        await db_.categories.add_bulk(categories)
        await db_.expenses.add_bulk(expenses)
        await db_.commit()


@pytest_asyncio.fixture(scope="session")
async def ac():
    headers = {
        "X-API-KEY": settings.API_KEY,
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as ac:
        yield ac


user_counter = 0


@pytest.fixture
async def user(ac):
    global user_counter
    user_counter += 1
    resp = await ac.post("/users/", json={
        "telegram_id": 777000111 + user_counter,
        "username": "fixture_user",
        "first_name": "Fixture",
        "last_name": "User"
    })
    return resp.json()


@pytest.fixture
async def category(ac, user):
    resp = await ac.post("/categories/", json={
        "title": "Fixture category",
        "user_id": user["id"]
    })
    return resp.json()


@pytest.fixture
async def expense(ac, user, category):
    resp = await ac.post("/expenses/", json={
        "user_id": user["id"],
        "category_id": category["id"],
        "amount": 12.50,
        "description": "Fixture expense"
    })
    return resp.json()
