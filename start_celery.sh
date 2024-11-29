# 1. Запуск Redis в режиме демона
echo "Starting Redis server..."
redis-server --daemonize yes

# 2. Запуск worker
echo "Starting worker"
celery -A task_manager.celery_app worker --loglevel=INFO &

# Ждем немного, чтобы worker успел запуститься
sleep 5

# 3. Запуск beater
echo "Starting beater"
celery -A task_manager.celery_app beat --loglevel=INFO



