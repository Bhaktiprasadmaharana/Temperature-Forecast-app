#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit

pip install -r requirements.txt

cd weatherproject
python manage.py collectstatic --no-input
