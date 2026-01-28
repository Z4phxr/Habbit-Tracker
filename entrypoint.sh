
#!/bin/sh
set -e

# Short pause to allow dependent services to start
sleep 3

# Railway/Render: PORT z ENV
export PORT=${PORT:-8000}

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
