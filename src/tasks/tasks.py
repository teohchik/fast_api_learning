import time

from src.tasks.celery_app import celery_inst


@celery_inst.task
def test_task():
    time.sleep(5)
    print("Testing task")
    return "This is a test task."