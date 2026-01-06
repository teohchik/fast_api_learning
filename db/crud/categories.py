from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories.categories import CategoriesRepository
from schemas.category import CategoryResponse, CategoryCreate


async def get_category_db(pagination, user_id: int, db: AsyncSession) -> list[CategoryResponse]:
    categories = await CategoriesRepository(db).get_all(pagination)
    if not categories:
        raise HTTPException(status_code=404, detail="Category not found")
    return [
        CategoryResponse.model_validate(category)
        for category in categories
    ]


async def create_category_db(data: CategoryCreate, db: AsyncSession):
    try:
        category = await CategoriesRepository(db).add(data)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(404, "User not found")

    return CategoryResponse.model_validate(category)
