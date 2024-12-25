#!/bin/bash

echo "Starting build process for Django..."
# Install Python dependencies
pip3 install -r requirements.txt


# Collect static files for production
python3 manage.py collectstatic --noinput

# Apply database migrations (for Vercel deployment)
python3 manage.py migrate