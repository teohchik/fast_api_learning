from datetime import datetime, date, timedelta

from sqlalchemy import select, func

from src.db.db_manager import DBManager
from src.db.models import Category, Expense
from src.db.session import AsyncSessionLocalNullPool


def get_previous_month_range():
    today = date.today()
    first_day_current_month = today.replace(day=1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    start_previous_month = last_day_previous_month.replace(day=1)

    return (
        datetime.combine(start_previous_month, datetime.min.time()),
        datetime.combine(first_day_current_month, datetime.min.time()),
    )


async def send_stats_to_all_users():
    month_start, month_end = get_previous_month_range()
    async with DBManager(session_factory=AsyncSessionLocalNullPool) as db:
        users = await db.users.get_users()

        for user in users:
            count_stmt = (
                select(func.count(Expense.id))
                .where(
                    Expense.user_id == user.id,
                    Expense.created_at >= month_start,
                    Expense.created_at < month_end,
                )
            )

            expenses_count = await db.session.scalar(count_stmt)

            if expenses_count < 2:
                print(f"User {user.id} has no expenses")
                continue

            stats_stmt = (
                select(
                    Category.title,
                    func.sum(Expense.amount).label("total")
                )
                .join(Category, Expense.category_id == Category.id)
                .where(
                    Expense.user_id == user.id,
                    Expense.created_at >= month_start,
                    Expense.created_at < month_end,
                )
                .group_by(Category.title)
            )

            result = await db.session.execute(stats_stmt)
            stats = result.all()

            # -------- 3. Тут відправка статистики --------
            # send_message(user.telegram_id, stats)
            for stat in stats:
                print(f"Category: {stat.title}, Total: {stat.total}")
