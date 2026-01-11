from datetime import datetime

from sqlalchemy import select

from src.api.deps import PaginationParams
from src.db.models import Expense
from src.db.repositories.base import BaseRepository
from src.schemas.expense import ExpenseResponse


class ExpensesRepository(BaseRepository):
    model = Expense
    schema = ExpenseResponse

    async def get_by_user_and_date(
            self,
            user_id: int,
            date_from: datetime | None = None,
            date_to: datetime | None = None,
            pagination: PaginationParams | None = None
    ):
        stmt = select(self.model).where(self.model.user_id == user_id)

        if date_from:
            stmt = stmt.where(self.model.created_at >= date_from)
        if date_to:
            stmt = stmt.where(self.model.created_at < date_to)

        if pagination:
            stmt = (stmt
                    .limit(pagination.per_page)
                    .offset((pagination.page - 1) * pagination.per_page))

        results = await self.session.execute(stmt)
        return [self.schema.model_validate(result) for result in results.scalars().all()]

    async def get_last_month_expenses(self, user_id: int, pagination: PaginationParams | None = None):
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        if now.month == 12:
            start_of_next_month = datetime(now.year + 1, 1, 1)
        else:
            start_of_next_month = datetime(now.year, now.month + 1, 1)

        return await self.get_by_user_and_date(
            user_id=user_id,
            date_from=start_of_month,
            date_to=start_of_next_month,
            pagination=pagination
        )

    async def get_expenses_for_month(self, user_id: int, year: int, month: int, pagination=None):
        start_of_month = datetime(year, month, 1)
        if month == 12:
            start_of_next_month = datetime(year + 1, 1, 1)
        else:
            start_of_next_month = datetime(year, month + 1, 1)

        return await self.get_by_user_and_date(
            user_id=user_id,
            date_from=start_of_month,
            date_to=start_of_next_month,
            pagination=pagination
        )
