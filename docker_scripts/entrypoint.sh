#!/bin/sh

set -e

echo "📦 اجرای migrate..."
python manage.py migrate --noinput

echo "🧱 اجرای collectstatic..."
python manage.py collectstatic --noinput

exec "$@"