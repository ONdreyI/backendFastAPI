# Hottels Backend (FastAPI)

## Описание Проекта

Этот проект представляет собой бэкенд-сервис для системы бронирования отелей, разработанный с использованием фреймворка FastAPI. Он предоставляет API для управления отелями, номерами, бронированиями, пользователями, а также для аутентификации и загрузки изображений. Проект использует PostgreSQL в качестве базы данных, Redis для кэширования и Celery для фоновых задач.

## Стек Технологий

- **FastAPI**: Современный, быстрый (высокопроизводительный) веб-фреймворк для создания API на Python 3.7+.
- **PostgreSQL**: Мощная, объектно-реляционная система управления базами данных.
- **SQLAlchemy**: Python SQL Toolkit и Object Relational Mapper (ORM).
- **Alembic**: Легкий инструмент для миграции баз данных для SQLAlchemy.
- **Redis**: Хранилище данных в памяти, используемое для кэширования.
- **Celery**: Распределенная очередь задач для Python.
- **Docker/Docker Compose**: Инструменты для контейнеризации и оркестрации приложений.
- **Nginx**: Веб-сервер и обратный прокси-сервер.

## Установка и Запуск

Для запуска проекта вам потребуется установленный Docker и Docker Compose.

### 1. Клонирование репозитория

```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd backendFastAPI
```

### 2. Настройка Git (опционально)

```bash
git config user.name "Andrey Ivanov"
git config user.email "ai3501669@gmail.com"
```

### 3. Запуск с помощью Docker Compose

Создайте Docker сеть:

```bash
docker network create myNetwork
```

Запустите все сервисы (база данных, кэш, бэкенд, Celery worker, Celery beat, Nginx):

```bash
docker-compose up --build -d
```

Если вы хотите запустить сервисы по отдельности, используйте следующие команды:

#### База данных (PostgreSQL)

```bash
docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16
```

#### Кэш (Redis)

```bash
docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis
```

#### Бэкенд (FastAPI)

Перед запуском бэкенда убедитесь, что образ `booking_image` собран. Это происходит при `docker-compose up --build`.

```bash
docker run --name booking_back \
    -p 7777:8000 \
    --network=myNetwork \
    booking_image
```

#### Celery Worker

```bash
docker run --name booking_celery_worker \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO
```

#### Celery Beat

```bash
docker run --name booking_celery_beat \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B
```

#### Nginx

Без SSL (http):

```bash
docker run --name booking_nginx \
    --volume ${PWD}/nginx.conf:/etc/nginx/nginx.conf \
    --network=myNetwork \
    -d -p 80:80 nginx
```

## Структура Проекта
'''
