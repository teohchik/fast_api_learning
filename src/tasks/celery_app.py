from celery import Celery

from src.config.settings import settings

celery_inst = Celery('tasks',
                    broker=settings.REDIS_URL,
                    include=['src.tasks.tasks']
                    )
