#!/bin/sh
set -e

until python -c "import socket; s = socket.socket(); s.connect(('${POSTGRES_HOST:-db}', int('${POSTGRES_PORT:-5432}'))); s.close()" 2>/dev/null; do
  sleep 1
done

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
