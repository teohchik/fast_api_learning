import logging
from typing import Iterable

from asyncpg import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from exceptions import (
    ObjectNotFoundException,
    IntegrityViolationException,
    ObjectAlreadyExistsException,
    ForeignKeyViolationException,
)
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

    async def get_by_filters(
        self, pagination: PaginationParams | None = None, order_by=None, **filters
    ):
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        if pagination is not None:
            stmt = stmt.limit(pagination.per_page).offset(
                (pagination.page - 1) * pagination.per_page
            )
        db_objs = await self.session.execute(stmt)
        return [self.mapper.map_to_domain_entity(db_obj) for db_obj in db_objs.scalars().all()]

    async def add(self, data: BaseModel):
        db_obj = self.model(**data.model_dump())
        self.session.add(db_obj)
        try:
            await self.session.flush()
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                logging.error(f"Cannot add object to DB, data = {data.model_dump()} Error: {ex}")
                raise ForeignKeyViolationException
            elif isinstance(ex.orig.__cause__, UniqueViolationError):
                logging.error(f"Cannot add object to DB, data = {data.model_dump()} Error: {ex}")
                raise ObjectAlreadyExistsException
            else:
                logging.error(f"Unexpected integrity error, data = {data.model_dump()} Error: {ex}")
                raise IntegrityViolationException

        return self.mapper.map_to_domain_entity(db_obj)

    async def add_bulk(self, data_list: Iterable[BaseModel]):
        db_objs = [self.model(**data.model_dump()) for data in data_list]
        self.session.add_all(db_objs)
        await self.session.flush()
        return [self.mapper.map_to_domain_entity(db_obj) for db_obj in db_objs]

    async def edit_by_id(self, data: BaseModel, obj_id: int):
        query = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            logging.error(
                f"Cannot edit object, id = {obj_id} data = {data.model_dump()} Error: Object not found"
            )
            raise ObjectNotFoundException

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(db_obj, key, value)

        await self.session.flush()
        return self.mapper.map_to_domain_entity(db_obj)

    async def delete_by_id(self, obj_id: int) -> None:
        query = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            logging.error(f"Cannot delete object, id = {obj_id} Error: Object not found")
            raise ObjectNotFoundException
        user_id = db_obj.user_id

        await self.session.delete(db_obj)
        return user_id
