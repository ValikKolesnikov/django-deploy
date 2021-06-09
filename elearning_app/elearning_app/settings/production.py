from .base import *
from .base import env

SECRET_KEY = env.str('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])
DATABASES['default'] = env.db('DATABASE_URL')
