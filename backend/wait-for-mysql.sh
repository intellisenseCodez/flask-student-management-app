#!/bin/bash

echo "Installing mysql-client (for mysqladmin)..."
if ! command -v mysqladmin &> /dev/null; then
    if [ -f /etc/debian_version ]; then
        apt-get update -y && apt-get install -y default-mysql-client
    elif [ -f /etc/alpine-release ]; then
        apk add --no-cache mysql-client
    elif [ -f /etc/redhat-release ]; then
        yum install -y mysql
    else
        echo "Unsupported OS. Install mysql-client manually."
        exit 1
    fi
fi

echo "Waiting for MySQL to become healthy..."

until mysqladmin ping -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
    sleep 2
done

echo "MySQL is up!"
exec "$@"