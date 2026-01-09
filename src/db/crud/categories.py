from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.categories import CategoriesRepository
from src.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate


async def get_category_by_user_db(pagination, user_id: int, db: AsyncSession) -> list[CategoryResponse]:
    categories = await CategoriesRepository(db).get_by_user_id(user_id, pagination)
    if not categories:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories


async def create_category_db(data: CategoryCreate, db: AsyncSession):
    try:
        category = await CategoriesRepository(db).add(data)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=404, detail="User not found")

    return category

async def update_category_db(category_id: int, data: CategoryUpdate, db: AsyncSession) -> CategoryResponse:
    try:
        category = await CategoriesRepository(db).edit_by_id(data, category_id)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=404, detail="Category not found")

    return category
