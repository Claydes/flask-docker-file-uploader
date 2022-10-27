
from celery import Celery
from celery.schedules import crontab
from mongo_client import MongoClient

db = MongoClient()
simple_app = Celery('worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

simple_app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'tasks.drop_database',
        'schedule': crontab(minute='*/1'),
    },
}


@simple_app.task
def drop_database():
    db.drop()

