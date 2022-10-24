
from celery import Celery


simple_app = Celery('tasks', broker='redis://172.18.0.2:6379/0', backend='redis://172.18.0.2:6379/0')


@simple_app.task
def longtime_add(x, y):
    return x + y