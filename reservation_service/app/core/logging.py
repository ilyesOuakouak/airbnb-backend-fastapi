from loguru import logger
import sys
import os


LOG_LEVEL = "INFO"
SERVICE_NAME = os.getenv("SERVICE_NAME", "main_api")

# Remove default handlers
logger.remove()

# Add JSON formatter for structured logs
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[service]} | {message}",
    level=LOG_LEVEL,
    serialize=True,   # JSON logs
)

# Optional: Write logs to a rotating file
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    level=LOG_LEVEL,
    serialize=True,
)


def get_logger():
    return logger.bind(service=SERVICE_NAME)
