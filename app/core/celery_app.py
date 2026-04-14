from celery import Celery
from app.core.config import settings

# 1. Initialize Celery
# 'worker' is just the name of the internal app
# broker=... tells Celery where to CONNECT to find the queue (Redis)
celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.email_tasks"]
)

# 2. Standard Configuration (Use JSON for safety)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# 3. Tell Celery where to look for tasks (we will create this folder next)
celery_app.autodiscover_tasks(["app.tasks"])