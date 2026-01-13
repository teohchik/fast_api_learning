from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.api.deps import PaginationParams
from src.db.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_one_or_none(self, **filters):
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        db_obj = await self.session.execute(stmt)
        db_obj = db_obj.scalar_one_or_none()
        if db_obj is None:
            return None
        return self.mapper.map_to_domain_entity(db_obj)

    async def get_by_filters(self, pagination: PaginationParams | None = None, order_by=None, **filters):
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
        db_objs = await self.session.execute(stmt)
        return [self.mapper.map_to_domain_entity(db_obj) for db_obj in db_objs.scalars().all()]

    async def add(self, data: BaseModel):
        db_obj = self.model(**data.model_dump())
        self.session.add(db_obj)
        await self.session.flush()
        return self.mapper.map_to_domain_entity(db_obj)

    async def edit_by_id(self, data: BaseModel, obj_id: int):
        query = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            raise NoResultFound(f"{self.model.__name__} not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(db_obj, key, value)

        await self.session.flush()
        return self.mapper.map_to_domain_entity(db_obj)
