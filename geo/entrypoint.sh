#!/bin/bash
echo "Waiting for PGSQL server..."
while ! nc -z geo_db 5432; do sleep 1; done;
echo "PGSQL server started"


python manage.py migrate
python manage.py collectstatic --no-input
if [ "$PRODUCTION" = "True" ]; then
    gunicorn config.wsgi:application --bind 0.0.0.0:8000
else
    gunicorn config.wsgi:application --bind 0.0.0.0:8000 --reload
fi
