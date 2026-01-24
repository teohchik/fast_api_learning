from typing import TypeAlias, Annotated

from fastapi import Depends

from src.db.db_manager import DBManager
from src.db.session import AsyncSessionLocal


async def get_db():
    async with DBManager(session_factory=AsyncSessionLocal) as db:
        yield db


DBDep: TypeAlias = Annotated[DBManager, Depends(get_db)]
