#!/bin/bash
# Set default port if not already set
export PORT=${PORT:-7222}

# Run your application
exec python manage.py runserver 0.0.0.0:$PORT

