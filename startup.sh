#!/bin/bash

# Apply database migrations
echo "Running migrations..."
python3 manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Migration failed."
    exit 1
fi

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --no-input
if [ $? -ne 0 ]; then
    echo "Error: Collecting static files failed."
    exit 1
fi

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn --workers 2 gallery.wsgi:application --bind 0.0.0.0:8000
