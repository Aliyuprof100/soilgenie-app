#!/bin/bash
set -e

# Change to the src directory where the code actually lives
cd /opt/render/project/src

# Now that we are in the right place, the commands will work
export FLASK_APP=run.py

echo "==> Running database migrations..."
flask db upgrade

echo "==> Starting Gunicorn server..."
gunicorn run:app