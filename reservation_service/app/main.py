from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import reservation
from app.core.database import Base, sync_engine
from app.core.logging import get_logger
from prometheus_fastapi_instrumentator import Instrumentator


logger = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 main_api service started (lifespan)")

    yield  # ← App runs here

    # Shutdown
    logger.info("🛑 main_api service stopped (lifespan)")


app = FastAPI(title="Reservation Microservice")

app.include_router(reservation.router)

Base.metadata.create_all(bind=sync_engine)

# PROMETHEUS METRICS
Instrumentator().instrument(app).expose(
    app,
    include_in_schema=False,
    endpoint="/metrics"
)

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"service": "reservation", "status": "running"}
