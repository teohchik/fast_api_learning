from fastapi import APIRouter, Query, status, Request
from fastapi_cache.decorator import cache

from src.api.deps import PaginationDep
from src.cache.expenses import ExpensesCacheKeyBuilder
from src.db.crud.expenses import get_expense_db, get_expenses_by_user_db, add_expense_db, update_expense_db, \
    delete_expense_db
from src.db.deps import DBDep
from src.init import redis_manager
from src.schemas.expense import (
    ExpenseResponse, ExpenseCreate, ExpenseUpdate,
)

expenses_router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@expenses_router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
        expense_id: int,
        db: DBDep):
    return await get_expense_db(expense_id, db)

@expenses_router.get("user/{user_id}", response_model=list[ExpenseResponse])
@cache(expire=ExpensesCacheKeyBuilder.expire, key_builder=ExpensesCacheKeyBuilder.build)
async def get_expenses(
    user_id: int,
    pagination: PaginationDep,
    db: DBDep,
    request: Request,
    year: int | None = Query(None, ge=2000, le=2100),
    month: int | None = Query(None, ge=1, le=12)
):
    return await get_expenses_by_user_db(db=db, pagination=pagination, user_id=user_id, year=year, month=month)


@expenses_router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
        expense_data: ExpenseCreate,
        db: DBDep
):
    response = await add_expense_db(expense_data, db)
    await redis_manager.scan_delete(pattern=ExpensesCacheKeyBuilder.generate_pattern(response.user_id))
    return response


@expenses_router.patch("/", response_model=ExpenseResponse)
async def update_expense(
        expense_id: int,
        update_data: ExpenseUpdate,
        db: DBDep):
    response = await update_expense_db(expense_id, update_data, db)
    await redis_manager.scan_delete(pattern=ExpensesCacheKeyBuilder.generate_pattern(response.user_id))
    return response

@expenses_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int, db: DBDep):
    user_id = await delete_expense_db(expense_id, db)
    await redis_manager.scan_delete(pattern=ExpensesCacheKeyBuilder.generate_pattern(user_id))
    return {"message": "Expense deleted successfully"}