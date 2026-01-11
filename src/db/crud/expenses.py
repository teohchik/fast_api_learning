from fastapi import HTTPException

from src.db.db_manager import DBManager
from src.schemas.expense import ExpenseResponse


async def get_expense_db(expense_id: int, db: DBManager) -> ExpenseResponse:
    response = await db.expenses.get_one_or_none(id=expense_id)
    if not response:
        raise HTTPException(status_code=404, detail="Expense not found")
    return response


async def get_expenses_by_user_db(pagination, db: DBManager, user_id: int, year: int, month: int) -> list[
    ExpenseResponse]:
    if year and month:
        response = await db.expenses.get_expenses_for_month(user_id=user_id,
                                                            year=year,
                                                            month=month,
                                                            pagination=pagination)

    else:
        response = await db.expenses.get_last_month_expenses(user_id=user_id,
                                                             pagination=pagination)
    return response


async def add_expense_db(expense_data, db: DBManager) -> ExpenseResponse:
    try:
        db_expense = await db.expenses.add(expense_data)
        await db.commit()
    except Exception as exc:
        print("Error occurred while adding a new expense:", exc)
        raise HTTPException(
            status_code=409,
            detail="Expense or User not found."
        )
    return db_expense
