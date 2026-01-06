from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from api.dependencies import PaginationParams


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_by_filters(
            self, filters: dict | None = None,
            pagination: PaginationParams | None = None,
            order_by=None):
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        if pagination is not None:
            stmt = (
                stmt
                .limit(pagination.per_page)
                .offset((pagination.page - 1) * pagination.per_page)
            )
        result = await self.session.execute(stmt)
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
