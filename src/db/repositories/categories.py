from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

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
            visible=True
        )

    async def delete_by_id(self, category_id: int):
        query = select(self.model).where((self.model.id == category_id) & (self.model.visible == True))

        result = await self.session.execute(query)
        db_obj = result.scalar_one_or_none()

        if not db_obj:
            raise NoResultFound(f"Category {category_id} not found")

        # Soft delete
        db_obj.visible = False
        await self.session.flush()  # commit робиться зовні
        return self.schema.model_validate(db_obj)
