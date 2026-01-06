from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, pagination=None):
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

    async def edit_by_id(self, data: BaseModel, obj_id: int):
        query = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            raise NoResultFound(f"{self.model.__name__} not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(db_obj, key, value)

        await self.session.flush()
        return db_obj
