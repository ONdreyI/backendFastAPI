from time import sleep

from backendCourse.src.tasks.celery_app import celery_instance


@celery_instance.tasks
def test_task():
    sleep(5)
    print("Я МОЛОДЕЦ!!!")
