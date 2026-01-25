import asyncio
from datetime import date

from src.services.stats_service import send_stats_to_all_users
from src.tasks.celery_app import celery_inst


@celery_inst.task(name='test')
def daily_stats_celery():
    asyncio.run(send_stats_to_all_users())


@celery_inst.task(name='monthly_stats')
def monthly_stats_celery():
    today = date.today()

    if today.day == 1:
        asyncio.run(send_stats_to_all_users())
