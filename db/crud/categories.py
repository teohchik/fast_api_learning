from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.categories import Category
from db.models.users import User
from schemas.category import CategoryResponse, CategoryCreate


async def get_category_db(user_id: int, db: AsyncSession, ) -> list[CategoryResponse]:
    query = select(Category).where(Category.user_id == user_id)
    result = await db.execute(query)

    categories = result.scalars().all()  # 🔥 ГОЛОВНЕ

    if not categories:
        raise HTTPException(status_code=404, detail="Category not found")

    return [
        CategoryResponse.model_validate(category)
        for category in categories
    ]


async def create_category_db(new_category_data: CategoryCreate, db: AsyncSession) -> CategoryResponse:
    try:
        db_category = Category(**new_category_data.model_dump())
        user_id = db_category.user_id
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        db.add(db_category)
        await db.commit()
        print(f"Added new category with ID: {db_category.id}")
    except Exception as exc:
        await db.rollback()
        print("Error occurred while adding a new category:", exc)
        raise
    return CategoryResponse.model_validate(db_category)
