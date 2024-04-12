release: python manage.py makemigrations && python manage.py migrate

web: gunicorn ondego_api.wsgi
