#!/bin/bash

python manage.py collectstatic --no-input --clear
python manage.py migrate
gunicorn elearning_app.wsgi:application --bind 0.0.0.0:8000


