from celery import Celery
from celery.schedules import crontab
import logging
from middleware.db_ops import SalesReader, ReportWriter
from model import Report
from settings import ServerSettings
from middleware.llm import ReportProcessor
from datetime import date

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация Celery
celery_app = Celery(
    "task_manager",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)
celery_app.autodiscover_tasks(["task_manager"])

celery_app.conf.update(
    enable_utc=False,
    beat_schedule={
        "generate_daily_report": {
            "task": "task_manager.generate_report",
            "schedule": crontab(hour=23, minute=55),
        },
    },
)


@celery_app.task
def generate_report():
    logger.info("Starting task generate_report")
    try:
        logger.info("LLM is preparing report")
        neuro = ReportProcessor(api_key=ServerSettings.LLM_API_KEY)
        report = neuro.report(SalesReader().read_by_date(date.today()))
        ReportWriter().write(Report(id=1, date=date.today(), report=report))
        logger.info("Report successfully generated: %s", report)
    except Exception as e:
        logger.error("Failed to generate report: %s", str(e))
