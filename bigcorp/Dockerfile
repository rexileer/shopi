FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Обновляем пакеты и устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libpq-dev \
    gobject-introspection libpango-1.0-0 libpangoft2-1.0-0 \
    netcat-openbsd \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt .  

# Копируем entrypoint.sh в контейнер
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Устанавливаем зависимости
RUN python -m pip install --upgrade pip --no-warn-script-location \
    && pip install -r requirements.txt --no-cache-dir --no-warn-script-location

# Копируем остальные файлы после установки зависимостей
COPY . .
