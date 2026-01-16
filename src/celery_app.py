import os
from celery import Celery

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

celery = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["src.tasks.deribit"],
)

celery.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "src.tasks.deribit.collect_prices",
        "schedule": 60.0,
    }
}
