#!/bin/bash

set -e

# we dont need to collectstatic each time
# python manage.py collectstatic --noinput
bash wait-for-it.sh db:5432
uwsgi --socket :${DJANGO_PORT} \
  --workers 4 \
  --master \
  --enable-threads \
  --module twentythirty.wsgi
