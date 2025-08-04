#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Set the FLASK_APP environment variable for this script's session
export FLASK_APP=run:app

# Run Flask database migrations
echo "Running database migrations..."
flask db upgrade

# Start the Gunicorn server, pointing to the app object in run.py
echo "Starting Gunicorn server..."
gunicorn run:app