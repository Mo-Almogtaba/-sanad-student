#!/bin/bash
set -e

echo "🔄 تشغيل Migrations..."
python manage.py migrate --noinput

echo "📦 جمع الملفات الثابتة..."
python manage.py collectstatic --noinput

echo "🚀 تشغيل gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
