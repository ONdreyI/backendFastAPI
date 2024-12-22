# Используем базовый образ Python 3.11.9
FROM python:3.11.9

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gnupg \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138 \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 0E98404D386FA1D9 \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 605C66F00D6C9793 \
    && apt-get update && \
    apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование requirements.txt и установка пакетов с использованием кэша
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов
COPY . .

# Команда для запуска приложения
CMD ["sh", "-c", "alembic upgrade head; python src/main.py"]
