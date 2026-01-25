from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.db.db_manager import DBManager
from src.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate


async def get_category_db(category_id: int, db: DBManager) -> CategoryResponse:
    category_response = await db.categories.get_one_or_none(id=category_id)
    if not category_response:
        raise HTTPException(status_code=404, detail="Category not found")
    return category_response


async def get_category_by_user_db(
    pagination, user_id: int, db: DBManager
) -> list[CategoryResponse]:
    categories = await db.categories.get_by_user_id(user_id, pagination)
    if not categories:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories


async def create_category_db(data: CategoryCreate, db: DBManager):
    try:
        category = await db.categories.add(data)
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404, detail="User not found")

    return category


async def update_category_db(
    category_id: int, data: CategoryUpdate, db: DBManager
) -> CategoryResponse:
    try:
        category = await db.categories.edit_by_id(data, category_id)
        await db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


async def delete_category_db(category_id: int, db: DBManager) -> CategoryResponse:
    try:
        category = await db.categories.delete_by_id(category_id)
        await db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Category not found")

    return category
