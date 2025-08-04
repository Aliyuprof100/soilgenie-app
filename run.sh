#!/bin/bash

set -e

# Tell the Flask CLI where to find the application factory
export FLASK_APP="soilgenie:create_app()"

# Run Flask database migrations
echo "Running database migrations..."
flask db upgrade

# Start the Gunicorn server pointing to the wsgi.py file
echo "Starting Gunicorn server..."
gunicorn wsgi:app