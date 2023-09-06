#!/bin/bash

set -m # to make job control work
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn project.wsgi -b 0.0.0.0:8000 --access-logfile - &
supercronic /app/crontab &
fg %1 # gross!
