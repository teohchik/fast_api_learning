from fastapi import FastAPI

from models import Expense, User, Category

app = FastAPI()


@app.get("/")
def test():
    return "barabola"


user_1 = User(id=1, telegram_id=123456, username="johndoe", first_name="John")
category_1 = Category(id=1, title="Food", user_id=user_1)

user_2 = User(id=2, telegram_id=654321, username="janedoe", first_name="Jane")
category_2 = Category(id=2, title="Transport", user_id=user_2)

expenses = [
    Expense(id=1, user_id=user_1, category_id=category_1, amount=10.5, description="Lunch"),
    Expense(id=2, user_id=user_1, category_id=category_1, amount=5.0, description="Snack"),
    Expense(id=3, user_id=user_1, category_id=category_1, amount=20.0, description="Dinner"),
    Expense(id=4, user_id=user_2, category_id=category_2, amount=15.0, description="Taxi"),
    Expense(id=5, user_id=user_2, category_id=category_2, amount=7.5, description="Bus Ticket"),
]

@app.get("/expenses/{telegram_id}")
def get_expenses_by_user(telegram_id: int):
    user_expenses = []
    for expense in expenses:
        if expense.user_id.telegram_id == telegram_id:
            user_expenses.append(expense)
    if not user_expenses:
        return "No expenses found"
    return user_expenses

@app.get("/expenses")
def get_all_expenses():
    return expenses

@app.post("/user")
def create_user(new_user: User):
    return new_user


if __name__ == '__main__':
    test()
