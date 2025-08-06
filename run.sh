#!/bin/bash

# Exit immediately if a command fails
set -e

# Add the current directory (which contains app.py, auth/, main/, etc.)
# to the list of places Python looks for code. This is the KEY.
export PYTHONPATH=$(pwd)

# Tell the Flask CLI that the app instance is in the app.py file
export FLASK_APP=app.py

# Run the database migrations. This command will now succeed.
echo "==> Running database migrations..."
flask db upgrade

# Start the Gunicorn production server. This command will also now succeed.
echo "==> Starting Gunicorn server..."
gunicorn app:app