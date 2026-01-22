import json

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.config.settings import settings
from src.db.base import Base
from src.db.db_manager import DBManager
from src.db.session import engine_null_pool, AsyncSessionLocalNullPool

from src.db.models import *
from src.main import app
from src.schemas.category import CategoryCreate
from src.schemas.expense import ExpenseCreate
from src.schemas.user import UserCreate


@pytest_asyncio.fixture
async def db():
    async with DBManager(session_factory=AsyncSessionLocalNullPool) as db:
        yield db


@pytest.fixture(autouse=True, scope="session")
def check_test_mode():
    assert settings.MODE == "TEST", "Tests must be run in TEST mode!"


@pytest.fixture(autouse=True, scope="session")
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/users.json", encoding="utf-8") as file_users:
        users = json.load(file_users)
    with open("tests/categories.json", encoding="utf-8") as file_categories:
        categories = json.load(file_categories)
    with open("tests/expenses.json", encoding="utf-8") as file_expenses:
        expenses = json.load(file_expenses)

    users = [UserCreate.model_validate(user) for user in users]
    categories = [CategoryCreate.model_validate(category) for category in categories]
    expenses = [ExpenseCreate.model_validate(expense) for expense in expenses]

    async with DBManager(session_factory=AsyncSessionLocalNullPool) as db_:
        await db_.users.add_bulk(users)
        await db_.categories.add_bulk(categories)
        await db_.expenses.add_bulk(expenses)
        await db_.commit()


@pytest_asyncio.fixture(scope="session")
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True, scope="session")
async def register_user(ac, setup_database):
    resp = await ac.post(url='/users/', json={"telegram_id": 543153452346, "username": "test1_user",
                                              "first_name": "Test User", "last_name": "Test User"})
    assert resp.status_code == 201
