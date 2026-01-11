from src.api.deps import PaginationParams
from src.db.models.categories import Category
from src.db.repositories.base import BaseRepository
from src.schemas.category import CategoryResponse


class CategoriesRepository(BaseRepository):
    model = Category
    schema = CategoryResponse

    async def get_by_user_id(self, user_id: int, pagination: PaginationParams | None = None):
        return await self.get_by_filters(
            pagination=pagination,
            order_by=Category.created_at,
            user_id=user_id,
        )
