#!/bin/bash
set -e
export FLASK_APP=run:app
export PYTHONPATH=$(pwd)
flask db upgrade
exec gunicorn run:app