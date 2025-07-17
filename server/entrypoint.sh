#!/bin/bash

# Exit on any error
set -e

# Set default port if not already set
export PORT=${PORT:-8000}

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

# Apply database migrations
echo "Applying database migrations..."
poetry run python manage.py migrate --noinput

# Collect static files (for production)
echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput || true

# Create superuser if it doesn't exist (optional)
echo "Creating superuser..."
poetry run python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
" || true

# Start server
echo "Starting Django server on port $PORT..."
exec poetry run python manage.py runserver 0.0.0.0:$PORT

