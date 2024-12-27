#!/bin/bash

python3 manage.py collectstatic && gunicorn --workers 2 gallery.wsgi