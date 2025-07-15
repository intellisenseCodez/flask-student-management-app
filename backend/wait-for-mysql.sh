#!/bin/sh

echo "Waiting for MySQL..."

while ! nc -z mysql-database 3306; do
  echo "MySQL is unavailable - sleeping"
  sleep 2
done

echo "MySQL is up - running migrations and starting app"
exec "$@"


#!/bin/sh

# Wait until MySQL is accepting connections
echo "Waiting for MySQL to be ready..."

for i in $(seq 1 30); do
  nc -z mysql-database 3306 && break
  echo "MySQL not yet available ($i/30) - sleeping..."
  sleep 2
done

if [ "$i" = 30 ]; then
  echo "Error: MySQL did not become ready in time."
  exit 1
fi

echo "MySQL is up. Executing: $@"
exec "$@"
