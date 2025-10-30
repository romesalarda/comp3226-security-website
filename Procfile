release: python manage.py migrate && python manage.py create_superuser_from_env
web: gunicorn core.wsgi:application
