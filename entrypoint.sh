#!/bin/sh
set -e

echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
while ! nc -z "${DB_HOST:-postgres}" "${DB_PORT:-5432}"; do
  sleep 1
done
echo "PostgreSQL is up."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn tourismo.wsgi:application \
  --config /app/gunicorn.conf.py
