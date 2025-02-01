# README: Shopi

## О проекте
**Shopi** – это современная e-commerce платформа, созданная на Django и Django REST Framework (DRF). Проект разработан с учетом удобства для пользователей и администраторов, предлагая гибкую систему управления товарами, корзиной и заказами.

## Технологический стек
- **Backend:** Django 5.1, Django REST Framework, Celery, Redis
- **База данных:** PostgreSQL
- **Кэширование и брокер задач:** Redis
- **Аутентификация:** Djoser, Simple JWT
- **Платежные системы:** Stripe, YooKassa
- **Фронтенд:** HTMX, Django Templates, Bootstrap 5
- **Деплой:** Docker, Gunicorn, Nginx

## Установка и запуск
### 1. Клонирование репозитория
```sh
git clone https://github.com/your-repo/shopi.git
cd shopi
```

### 2. Создание и настройка `.env` файла
Создайте файл `.env` в корневой директории и добавьте в него:
```ini
POSTGRES_DB=shopi_db
POSTGRES_USER=shopi_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
EMAIL_HOST_PASSWORD=your_email_password
STRIPE_PUBLISHABLE_KEY=your_stripe_pub_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WH_SECRET=your_stripe_webhook_secret
YOOKASSA_SECRET_KEY=your_yookassa_secret_key
YOOKASSA_SHOP_ID=your_yookassa_shop_id
```

### 3. Запуск проекта с Docker
```sh
docker-compose up --build -d
```

### 4. Применение миграций и сборка статики
```sh
docker exec -it bigcorp-backend python manage.py migrate
docker exec -it bigcorp-backend python manage.py collectstatic --noinput
```

### 5. Создание суперпользователя
```sh
docker exec -it bigcorp-backend python manage.py createsuperuser
```

## Основные фичи
- **Корзина и заказы**: пользователи могут добавлять товары в корзину и оформлять заказы.
- **Платежи**: интеграция с Stripe и YooKassa.
- **JWT-аутентификация**: безопасная регистрация и вход через Djoser.
- **Админ-панель**: управление заказами, товарами и пользователями.
- **Отзывы**: возможность оставлять отзыв для пользователей.
- **Фоновая обработка задач**: Celery + Redis.
- **HTMX**: улучшение пользовательского опыта без полной перезагрузки страницы.

## API Документация
После запуска проекта API документация доступна по адресу:
- **Swagger**: `http://localhost/api/docs/swagger/`
- **ReDoc**: `http://localhost/api/docs/redoc/`

## Разработка
### Запуск сервера локально (без Docker)
```sh
python manage.py runserver
```

### Запуск Celery
```sh
celery -A bigcorp worker --loglevel=info --beat
```

### Запуск тестов
```sh
python manage.py test
```

## Контакты
Если у вас есть вопросы или предложения, свяжитесь со мной через GitHub или email.

