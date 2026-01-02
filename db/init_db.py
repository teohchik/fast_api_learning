from db.base import Base
from db.session import engine
import db.models.users
import db.models.expenses
import db.models.categories


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
