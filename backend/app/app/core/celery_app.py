from celery import Celery
from app.core.config import settings

celery_app = Celery("worker", broker=settings.CELERY_BROKER, backend=settings.RESULT_BACKEND)
celery_app.conf.update(elasticsearch_save_meta_as_text=False, result_extended=True, enable_utc=True)
celery_app.conf.database_engine_options = {'echo': True}

celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue",
    "app.worker.get_address": "main-queue",
}
