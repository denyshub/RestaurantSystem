#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST 5432; do
  sleep 1
done

echo "Postgres started"

python user_service/manage.py migrate

exec "$@"
