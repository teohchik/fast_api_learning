from fastapi import APIRouter
from starlette import status

from schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)

expenses_router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@expenses_router.get("/{telegram_id}", response_model=list[ExpenseResponse])
def get_expenses_by_user(telegram_id: int):
    return "expenses by user"


@expenses_router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense_data: ExpenseCreate, telegram_id: int):
    # Here you would typically save the new expense to the database
    return {
        "id": 999,
        "telegram_id": telegram_id or 123,
        "category_id": expense_data.category_id,
        "amount": expense_data.amount,
        "description": expense_data.description,
        "created_at": "2025-12-31T23:59:59",
    }

@expenses_router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, update_data: ExpenseUpdate):
    # Here you would typically update the expense in the database
    return update_data

@expenses_router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    # Here you would typically delete the expense from the database
    return {"message": f"Expense with id {expense_id} deleted"}