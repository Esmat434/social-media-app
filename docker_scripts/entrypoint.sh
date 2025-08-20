#!/bin/sh

set -e

echo "📦 Applying database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "🧱 Collecting static files..."
python manage.py collectstatic --noinput

echo "👤 Creating superuser if it doesn't exist..."
python manage.py create_custom_superuser

exec "$@"