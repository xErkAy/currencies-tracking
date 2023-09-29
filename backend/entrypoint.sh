#!/bin/bash

until pg_isready -d "$DB_NAME" -h "$DB_HOST" -p 5432 -U "$DB_USER"; do
    echo "$(date) - waiting for postgres"
    sleep 5
done

function run_server() {
  python manage.py runserver 0.0.0.0:8000
}

if [[ ! -d "$LOGS_DIR" ]]; then
    mkdir -p "$LOGS_DIR"
fi

yes yes | python manage.py collectstatic && run_server
