#!/bin/bash
set -e

# Add the current directory to Python's path
export PYTHONPATH=$(pwd)

# Tell Flask where the app is
export FLASK_APP=app.py

# Run the database migrations
flask db upgrade

# Start the production server
gunicorn app:app