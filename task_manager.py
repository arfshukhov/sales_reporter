from celery import Celery, shared_task

from middleware.db_ops import SalesReader, ReportWriter
from settings import ServerSettings
from middleware.llm import ReportProcessor
from datetime import date
# Инициализация Celery
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',  # Укажите URL брокера сообщений
    backend='redis://localhost:6379/0'  # Опционально: для сохранения статусов задач
)

celery_app.conf.update(
    timezone='UTC+3',  # Укажите ваш часовой пояс
    enable_utc=True,
    beat_schedule={
        'generate_daily_report': {
            'task': 'tasks.generate_report',
            'schedule': {
            'type': 'crontab',
            'minute': 55,
            'hour': 23,
            }
        }
    }
)

@shared_task
def generate_report():
    neuro = ReportProcessor(
        api_key=ServerSettings.LLM_API_KEY
    )
    report = neuro.report(
        SalesReader().read_by_date(date.today())
    )
    ReportWriter().write(report)


