from fastapi import APIRouter, status, Request, Depends
from fastapi_cache.decorator import cache

from src.api.deps import PaginationDep, verify_bot_api_key
from src.cache.categories import CategoryCacheKeyBuilder
from src.db.crud.categories import (
    create_category_db,
    update_category_db,
    get_category_by_user_db,
    delete_category_db,
    get_category_db,
)
from src.db.deps import DBDep
from src.init import redis_manager
from src.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate

category_router = APIRouter(
    prefix="/categories", dependencies=[Depends(verify_bot_api_key)], tags=["Categories"]
)


@category_router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: DBDep):
    return await get_category_db(category_id, db)


@category_router.get("/", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
@cache(expire=CategoryCacheKeyBuilder.expire, key_builder=CategoryCacheKeyBuilder.build)
async def get_categories_by_user(
    pagination: PaginationDep, user_id: int, db: DBDep, request: Request
):
    return await get_category_by_user_db(pagination, user_id, db)


@category_router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(new_category_data: CategoryCreate, db: DBDep):
    response = await create_category_db(new_category_data, db)
    await redis_manager.scan_delete(
        pattern=CategoryCacheKeyBuilder.generate_pattern(response.user_id)
    )
    return response


@category_router.patch("/", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def update_category(category_id: int, update_data: CategoryUpdate, db: DBDep):
    response = await update_category_db(category_id, update_data, db)
    await redis_manager.scan_delete(
        pattern=CategoryCacheKeyBuilder.generate_pattern(response.user_id)
    )
    return response


@category_router.delete("/", response_model=CategoryResponse)
async def delete_category(category_id: int, db: DBDep):
    response = await delete_category_db(category_id, db)
    await redis_manager.scan_delete(
        pattern=CategoryCacheKeyBuilder.generate_pattern(response.user_id)
    )
    return response
