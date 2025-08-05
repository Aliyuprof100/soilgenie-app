#!/bin/bash

# This script is designed to run from the root of the project.
set -e

# Tell the Flask CLI that the app is inside the 'soilgenie' package
# and to find it using the factory pattern. This is the most robust method.
export FLASK_APP="soilgenie:create_app()"

# Tell Gunicorn to do the same, but also explicitly add the current
# directory to the Python path to resolve any ambiguity.
# The format is wsgi:app (filename:variable_name). We will use run.py
# as the entry point for gunicorn.

# Run Flask database migrations first.
echo "==> Running database migrations..."
flask db upgrade

# Now, start the Gunicorn server.
echo "==> Starting Gunicorn server..."
gunicorn --pythonpath . -w 4 run:app