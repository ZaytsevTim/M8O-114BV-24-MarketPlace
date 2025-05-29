FROM python:3.10-slim

# Устанавливаем зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .

# Используем gunicorn для продакшн-сервера
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
