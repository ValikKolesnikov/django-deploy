from .models import User
from celery import shared_task


@shared_task
def get_user_count():
    return f'Current user count: {User.objects.count()}'
