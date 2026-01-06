from typing import Annotated

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import PaginationParams, PaginationDep
from db.crud.categories import create_category_db, get_category_db
from db.deps import get_db
from schemas.category import CategoryResponse, CategoryCreate

category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@category_router.get("/", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_all_categories(pagination: PaginationDep, user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_category_db(pagination, user_id, db)


@category_router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(new_category_data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await create_category_db(new_category_data, db)
