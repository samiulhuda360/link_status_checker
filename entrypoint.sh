#!/bin/sh

# Wait for the database to be available if necessary
# python manage.py wait_for_db

python manage.py collectstatic --noinput
python manage.py migrate --noinput
# Start the main process
exec "$@"