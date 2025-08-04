#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Tell the Flask CLI to find the app using the factory function.
# This is the most robust method and solves the import error.
export FLASK_APP="soilgenie:create_app()"

# Run Flask database migrations. This command will now succeed.
echo "Running database migrations..."
flask db upgrade

# Start the Gunicorn server. This command is correct.
echo "Starting Gunicorn server..."
gunicorn run:app