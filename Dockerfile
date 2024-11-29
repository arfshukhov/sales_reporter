FROM python:3.13-slim

# Устанавливаем переменные среды
ENV HOST=0.0.0.0
ENV PORT=8888

# Устанавливаем рабочую директорию
WORKDIR /sales_reporter

RUN apt-get update && apt-get install -y \
    redis-server \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Скопируем файл зависимостей и установим их
COPY /requirements.txt /sales_reporter/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Копируем весь исходный код в контейнер
COPY . /sales_reporter
RUN chmod +x start_celery.sh
# Открываем порт для приложения
EXPOSE 6379
EXPOSE $PORT


# Запускаем приложение
CMD ["sh", "-c", "uvicorn --host $HOST --port $PORT main:app & ./start_celery.sh"]