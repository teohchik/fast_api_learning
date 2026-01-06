from pydantic import BaseModel
from sqlalchemy import select

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, pagination = None):
        query = select(self.model)
        if pagination is not None:
            per_page = pagination.per_page or 10
            query = (
                query
                .limit(per_page)
                .offset((pagination.page - 1) * per_page)
            )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, data: BaseModel):
        db_obj = self.model(**data.model_dump())
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj
