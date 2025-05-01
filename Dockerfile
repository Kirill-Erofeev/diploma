# Используем официальный минимальный образ Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    espeak \
    libespeak1 \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости без кэша
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код в контейнер
COPY . .

# Проверяем наличие SQLite-базы, если нет — предупреждаем
RUN ls app/database/sql_app.db || echo "⚠️ WARNING: DB not found"

# Открываем порт 8000
EXPOSE 8000

# Запускаем FastAPI-приложение
# CMD ["python", "app/main.py"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "./certs/key.pem", "--ssl-certfile", "./certs/cert.pem", "--reload"]