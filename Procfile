# Procfile para Django en Railway

web: \
mkdir -p /app/staticfiles /app/media && \
python manage.py collectstatic --noinput && \
gunicorn django_crud_api.wsgi:application --bind 0.0.0.0:$PORT
