release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn habits_project.wsgi --log-file -
