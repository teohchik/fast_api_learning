from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import PaginationDep
from src.db.crud.categories import create_category_db, update_category_db, get_category_by_user_db, delete_category_db
from src.db.deps import get_db, DBDep
from src.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate

category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@category_router.get("/",
                     response_model=list[CategoryResponse],
                     status_code=status.HTTP_200_OK)
async def get_categories_by_user(
        pagination: PaginationDep,
        user_id: int,
        db: DBDep
):
    return await get_category_by_user_db(pagination, user_id, db)


@category_router.post("/",
                      response_model=CategoryResponse,
                      status_code=status.HTTP_201_CREATED)
async def create_category(
        new_category_data: CategoryCreate,
        db: DBDep):
    return await create_category_db(new_category_data, db)


@category_router.patch("/",
                       response_model=CategoryResponse,
                       status_code=status.HTTP_200_OK)
async def update_category(
        category_id: int,
        update_data: CategoryUpdate,
        db: DBDep):
    return await update_category_db(category_id, update_data, db)


@category_router.delete("/", response_model=CategoryResponse)
async def delete_category(
        category_id: int,
        db: DBDep):
    return await delete_category_db(category_id, db)
