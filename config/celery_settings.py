import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

CELERY_RESULT_BACKEND = 'django-db'
BROKER_URL = 'redis://localhost:6379'

app = Celery('config', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND, result_backend='rpc://',
             include=['parser.tasks', ])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'upcoming_meetings_checker': {
        'task': 'parser.tasks.parse_logs',
        'schedule': 60,
        'args': (),
    },
}

# celery -A config worker -l INFO
# celery -A config beat -l INFO

