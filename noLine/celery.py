import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noLine.settings')

app = Celery('noLine')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'liningcheck': {
        'task': 'Transaction.tasks.lining',
        'schedule': 5,
    },
    'learnphase': {
        'task': 'Transaction.tasks.learn',
        'schedule': crontab(hour=0, minute=0,),
    },
}
