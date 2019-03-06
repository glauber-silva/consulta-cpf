#!/bin/sh

echo "Waiting for users ... "

while ! nc -z users 5002; do
    sleep 0.1
done

echo "PostgreSQL started"

python manage.py run -h 0.0.0.0