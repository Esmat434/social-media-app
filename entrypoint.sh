#!/bin/bash

# توقف اسکریپت در صورت خطا
set -e

echo "📦 run migrate..."
python manage.py migrate

echo "🧱 run collectstatic..."
python manage.py collectstatic --noinput

echo "🚀 run Gunicorn..."
exec gunicorn SocialMedia.wsgi:application --bind 0.0.0.0:8000