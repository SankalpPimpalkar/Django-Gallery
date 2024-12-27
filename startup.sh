#!/bin/bash

# Set up logging
exec > >(tee -a /var/log/app-runner.log|logger -t app-runner -s 2>/dev/console) 2>&1

echo "Starting deployment process..."

# Apply database migrations
echo "Running migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Migration failed."
    exit 1
fi

# Collect static files (consider using S3 for production)
echo "Collecting static files..."
python manage.py collectstatic --no-input
if [ $? -ne 0 ]; then
    echo "Error: Collecting static files failed."
    exit 1
fi

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn --workers ${GUNICORN_WORKERS:-2} \
    --log-level=info \
    --access-logfile=- \
    --error-logfile=- \
    gallery.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000}
