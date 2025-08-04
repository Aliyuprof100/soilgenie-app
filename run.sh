#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Run Flask database migrations
echo "Running database migrations..."
flask db upgrade

# Start the Gunicorn server
echo "Starting Gunicorn server..."
gunicorn run:app