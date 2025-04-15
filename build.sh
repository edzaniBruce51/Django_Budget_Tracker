#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations - run auth migrations first
python manage.py migrate auth --fake-initial
python manage.py migrate contenttypes --fake-initial
python manage.py migrate admin --fake-initial
python manage.py migrate sessions --fake-initial

# Then run all migrations
python manage.py migrate
