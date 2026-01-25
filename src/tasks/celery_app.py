from celery import Celery
from celery.schedules import crontab # noqa 401

from src.config.settings import settings

celery_inst = Celery('tasks',
                     broker=settings.REDIS_URL,
                     include=['src.tasks.tasks']
                     )

celery_inst.conf.beat_schedule = {
    "test": {
        "task": "test",
        "schedule": 10
    }
}
# celery_inst.conf.beat_schedule = {
#     "monthly_stats": {
#         "task": "monthly_stats",
#         "schedule": crontab(hour=10, minute=0),
#     }
# }
