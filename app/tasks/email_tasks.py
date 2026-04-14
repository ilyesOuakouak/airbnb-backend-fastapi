import time
from app.core.celery_app import celery_app
from celery.utils.log import get_task_logger

# Celery has its own logger that shows up nicely in the worker terminal
logger = get_task_logger(__name__)

@celery_app.task(name="send_reservation_email")
def send_reservation_email(email: str, reservation_id: int):
    """
    Simulate sending a configuration email.
    This mimics a slow external API call (  like SendGrid or AWS SES )
    """
    logger.info(f"[START] Sending email to {email} for reservation # {reservation_id} ...")

    # Simulate a 5-second delay (This would BLOCK the API if not Async)
    time.sleep(5)

    logger.info(f"✅ [DONE] Email sent successfully to {email}")

    return f"Email send to {email}"

