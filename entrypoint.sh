#!/bin/bash

set -e

echo "📦 اجرای migrate..."
python manage.py migrate --noinput

echo "🧱 اجرای collectstatic..."
python manage.py collectstatic --noinput

if [ "$DJANGO_ENV" = "production" ]; then
    echo "🚀 اجرای سرور در حالت Production با Gunicorn"
    exec gunicorn SocialMedia.wsgi:application --bind 0.0.0.0:8000
else
    echo "🚀 اجرای سرور در حالت Development با runserver"
    exec python manage.py runserver 0.0.0.0:8000
fi
