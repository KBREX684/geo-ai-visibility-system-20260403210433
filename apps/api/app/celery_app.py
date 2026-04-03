from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery = Celery(
    "geo_worker",
    broker=settings.broker_url,
    backend=settings.result_backend,
    include=["app.tasks"],
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
)

