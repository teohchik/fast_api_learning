from typing import TypeAlias, Annotated

from fastapi import Depends

from src.db.db_manager import DBManager
from src.db.session import AsyncSessionLocal


def get_db_manager():
    return DBManager(session_factory=AsyncSessionLocal)

async def get_db():
    async with get_db_manager() as db:
        yield db

DBDep: TypeAlias = Annotated[DBManager, Depends(get_db)]