from src.schemas.expense import ExpenseCreate, ExpenseUpdate


async def test_add_expense(db):
    user = (await db.users.get_users())[0]
    category = (await db.categories.get_by_filters(user_id=user.id))[0]
    # create
    expense_add = ExpenseCreate(
        user_id=user.id,
        category_id=category.id,
        amount=51.3,
        description="Test Expense",
    )
    new_expense = await db.expenses.add(expense_add)
    # get
    expense = await db.expenses.get_one_or_none(id=new_expense.id)
    assert expense
    assert expense.amount == new_expense.amount
    # update
    updated_expense_data = ExpenseUpdate(
        amount=22.2,
        description="Test Updated Expense",
    )
    updated_expense = await db.expenses.edit_by_id(data=updated_expense_data, obj_id=expense.id)
    assert updated_expense
    assert updated_expense.amount == updated_expense_data.amount
    # delete
    await db.expenses.delete_by_id(expense.id)
    expense = await db.expenses.get_one_or_none(id=new_expense.id)
    assert not expense
