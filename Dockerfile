# -----------------------------
# 1) Base image (small + secure)
# -----------------------------
FROM python:3.10-slim

# Prevents Python from writing .pyc files + ensures clean logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -----------------------------
# 2) Install system dependencies
# -----------------------------
# RUN apt-get update && apt-get install -y build-essential

# -----------------------------
# 3) Set working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# 4) Install dependencies early
# (keeps Docker layer cache efficient)
# -----------------------------
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# 5) Copy the whole codebase and .env
# -----------------------------
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY requirements.txt .
COPY .env.docker .env
# -----------------------------
# 6) Expose API port
# -----------------------------
EXPOSE 8000

# -----------------------------
# 7) Start FastAPI
# -----------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
