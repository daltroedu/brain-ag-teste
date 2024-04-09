#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ ! -z "$USER_ID" ] && [ ! -z "$GROUP_ID" ]; then
    chown -R $USER_ID:$GROUP_ID /usr/src/app
fi

exec "$@"