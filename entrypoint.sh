#!/bin/sh
# Container start-up: prepare the database and static files, then serve the site.

# Stop at the first failing command so Gunicorn never starts on a broken setup
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# exec replaces the shell with Gunicorn, so Docker's stop signals reach it directly
exec gunicorn oc_lettings_site.wsgi --bind 0.0.0.0:8000
