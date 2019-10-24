#!/bin/sh
source ../hireme_venv/bin/activate
flask db init
flask db migrate
flask db upgrade
# flask translate compile
exec gunicorn -b :5000 --workers=2 --threads=4 --worker-tmp-dir /dev/shm --access-logfile - --error-logfile - wsgi:app
