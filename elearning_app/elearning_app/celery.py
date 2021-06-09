import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_app.settings.local')

app = Celery('elearning_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'user_count_check': {
        'task': 'user.tasks.get_user_count',
        'schedule': 15
    }
}
