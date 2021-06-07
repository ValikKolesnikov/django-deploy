import string
from django.utils.crypto import get_random_string

from .models import Course, Category
from celery import shared_task


@shared_task
def create_random_courses(total):
    category = Category(title=get_random_string(10, string.ascii_letters))
    category.save()
    for number in range(total):
        Course.objects.create(
            title=get_random_string(10, string.ascii_letters),
            description=get_random_string(100, string.ascii_letters),
            category=category
        )
    return f'{total} courses created!'
