from src.db.models import Category, Expense, User
from src.db.repositories.mappers.base import DataMapper
from src.schemas.category import CategoryResponse
from src.schemas.expense import ExpenseResponse
from src.schemas.user import UserResponse


class CategoryDataMapper(DataMapper):
    model = Category
    schema = CategoryResponse


class ExpenseDataMapper(DataMapper):
    model = Expense
    schema = ExpenseResponse


class UserDataMapper(DataMapper):
    model = User
    schema = UserResponse
