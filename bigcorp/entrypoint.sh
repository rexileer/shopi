#!/bin/sh

echo "Ждём PostgreSQL..."
while ! nc -z db 5432; do sleep 1; done
echo "PostgreSQL доступен!"

# Дальше идёт запуск миграций и Gunicorn...

#!/bin/sh
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

exec gunicorn bigcorp.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 4 \
    --timeout 300 \
    --worker-class gthread


# Запускаем Stripe (если нужно)
stripe listen --forward-to localhost:8000/payment/webhook-stripe/
