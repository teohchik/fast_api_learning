from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.api.deps import PaginationParams
from src.db.models.categories import Category
from src.db.repositories.base import BaseRepository
from src.db.repositories.mappers.mappers import CategoryDataMapper


class CategoriesRepository(BaseRepository):
    model = Category
    mapper = CategoryDataMapper

    async def get_by_user_id(self, user_id: int, pagination: PaginationParams | None = None):
        return await self.get_by_filters(
            pagination=pagination, order_by=Category.created_at, user_id=user_id, visible=True
        )

    async def delete_by_id(self, category_id: int):
        query = select(self.model).where(
            (self.model.id == category_id) & (self.model.visible == True)
        )  # noqa: E712

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        if not model:
            raise NoResultFound(f"Category {category_id} not found")

        model.visible = False
        await self.session.flush()
        return self.mapper.map_to_domain_entity(model)
