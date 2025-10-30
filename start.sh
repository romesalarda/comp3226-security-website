#!/bin/bash

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser from environment..."
python manage.py create_superuser_from_env

echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application
