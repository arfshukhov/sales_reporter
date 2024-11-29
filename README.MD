# Sales Reporter



- Запускатеся через Docker

### Прописываем в директории проекта:
  `docker build -t sales_reporter .`

  `docker run -p 8888:8888 sales_reporter`

- Конфигурируется через переменные окружения (по умолчанию HOST=0.0.0.0, PORT=8888)
- все переменные лежат в файле .env
## Переменные окружения и их значения по умолчанию:
                    
Variable      | Value
------------- | -------------
HOST          | 0.0.0.0
PORT          | 8888
ENVIRONMENT   | local
DB_HOST       | localhost
DB_PORT       | 5432
DB_PASSWORD   | 12345678
DB_USER       | postgres
DB_NAME       | postgres
DB_KIND       | sqlite
LLM_API_KEY   |*Добавьте свой ключ авторизации GigaChat*

- Чтобы проект сервер присоединялся к базе Postgres измените DB_KIND на postgres

### P.S. Готов ответить на все вопросы по проекту на собеседовании