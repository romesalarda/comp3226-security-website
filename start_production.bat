@echo off
REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Apply database migrations
echo Applying database migrations...
python manage.py migrate --noinput

REM Start Gunicorn
echo Starting Gunicorn...
gunicorn core.wsgi:application --config gunicorn_config.py
