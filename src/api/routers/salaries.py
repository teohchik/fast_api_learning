from fastapi import APIRouter, Depends, Request, Query, status
from fastapi_cache.decorator import cache

from src.api.deps import verify_bot_api_key, PaginationDep
from src.cache.salaries import SalariesCacheKeyBuilder
from src.db.crud.salaries import (
    get_salary_db,
    get_salaries_by_user_db,
    add_salary_db,
    update_salary_db,
    delete_salary_db,
)
from src.db.deps import DBDep
from src.init import redis_manager
from src.schemas.salary import SalaryCreate, SalaryResponse, SalaryUpdate

salary_router = APIRouter(
    prefix="/salaries", dependencies=[Depends(verify_bot_api_key)], tags=["Salaries"]
)


@salary_router.get("/{salary_id}", response_model=SalaryResponse)
async def get_salary(salary_id: int, db: DBDep):
    return await get_salary_db(salary_id, db)


@salary_router.get("/user/{user_id}", response_model=list[SalaryResponse])
@cache(expire=SalariesCacheKeyBuilder.expire, key_builder=SalariesCacheKeyBuilder.build)
async def get_salaries(
    user_id: int,
    pagination: PaginationDep,
    db: DBDep,
    request: Request,
    year: int | None = Query(None, ge=2000, le=2100),
    month: int | None = Query(None, ge=1, le=12),
):
    return await get_salaries_by_user_db(
        db=db, pagination=pagination, user_id=user_id, year=year, month=month
    )


@salary_router.post("/", response_model=SalaryResponse, status_code=status.HTTP_201_CREATED)
async def create_salary(salary_data: SalaryCreate, db: DBDep):
    response = await add_salary_db(salary_data, db)
    await redis_manager.scan_delete(
        pattern=SalariesCacheKeyBuilder.generate_pattern(response.user_id)
    )
    return response


@salary_router.patch("/", response_model=SalaryResponse)
async def update_salary(salary_id: int, update_data: SalaryUpdate, db: DBDep):
    response = await update_salary_db(salary_id, update_data, db)
    await redis_manager.scan_delete(
        pattern=SalariesCacheKeyBuilder.generate_pattern(response.user_id)
    )
    return response


@salary_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_salary(salary_id: int, db: DBDep):
    user_id = await delete_salary_db(salary_id, db)
    await redis_manager.scan_delete(pattern=SalariesCacheKeyBuilder.generate_pattern(user_id))
    return {"message": "Salary deleted successfully"}
