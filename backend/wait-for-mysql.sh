#!/bin/bash

echo "Waiting for MySQL to become healthy..."

until mysqladmin ping -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
    sleep 2
done

echo "MySQL is up!"
exec "$@"