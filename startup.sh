#!/bin/bash
python manage.py collectstatic && gunicorn gallery.wsgi:application --bind 0.0.0.0:8000
