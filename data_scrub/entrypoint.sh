#!/bin/bash

set -e  # Stop script on error

if ! python manage.py migrate --noinput; then
  echo "Migrations failed"
  exit 1
fi

exec "$@"