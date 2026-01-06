from api.dependencies import PaginationParams
from db.models.categories import Category
from db.repositories.base import BaseRepository


class CategoriesRepository(BaseRepository):
    model = Category

    async def get_by_user_id(self, user_id: int, pagination: PaginationParams | None = None):
        return await self.get_by_filters(
            filters={"user_id": user_id},
            pagination=pagination,
            order_by=Category.created_at,
        )
