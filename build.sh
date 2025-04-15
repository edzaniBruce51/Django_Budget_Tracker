#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Create data directory for SQLite database
mkdir -p data
chmod 777 data

# Apply database migrations
python manage.py migrate

# Create superuser from environment variables if provided
python manage.py create_superuser_from_env
