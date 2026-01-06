from db.models.categories import Category
from db.repositories.base import BaseRepository


class CategoriesRepository(BaseRepository):
    model = Category