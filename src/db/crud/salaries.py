from fastapi import HTTPException

from exceptions import ForeignKeyViolationException, ObjectNotFoundException
from src.db.db_manager import DBManager
from src.schemas.salary import SalaryResponse, SalaryUpdate


async def get_salary_db(salary_id: int, db: DBManager) -> SalaryResponse:
    response = await db.salaries.get_one_or_none(id=salary_id)
    if not response:
        raise HTTPException(status_code=404, detail="Salary not found")
    return response


async def get_salaries_by_user_db(
    pagination, db: DBManager, user_id: int, year: int, month: int
) -> list[SalaryResponse]:
    if year is not None and month is not None:
        response = await db.salaries.get_salaries_for_month(
            user_id=user_id, year=year, month=month, pagination=pagination
        )

    else:
        response = await db.salaries.get_last_month_salaries(user_id=user_id, pagination=pagination)
    return response


async def add_salary_db(salary_data, db: DBManager) -> SalaryResponse:
    try:
        db_salary = await db.salaries.add(salary_data)
        await db.commit()
    except ForeignKeyViolationException:
        raise HTTPException(status_code=409, detail="Salary or User not found.")
    return db_salary


async def update_salary_db(salary_id: int, data: SalaryUpdate, db: DBManager) -> SalaryResponse:
    try:
        db_salary = await db.salaries.edit_by_id(data, salary_id)
        await db.commit()
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Salary not found")
    return db_salary


async def delete_salary_db(salary_id: int, db: DBManager) -> None:
    try:
        user_id = await db.salaries.delete_by_id(salary_id)
        await db.commit()
        return user_id
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Salary not found")
