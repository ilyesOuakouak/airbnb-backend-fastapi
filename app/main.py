from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import Base, sync_engine
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import user, listing, availability, reservation
from app.core.logging import get_logger

logger = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("main_api service started (lifespan)")

    yield  # ← App runs here

    # Shutdown
    logger.info("main_api service stopped (lifespan)")

app = FastAPI(title="AirBnb Backend")

# Register routers
app.include_router(user.router)
app.include_router(listing.router)
app.include_router(availability.router)
app.include_router(reservation.router)

# Temporary: auto-create tables for development (Alembic handles schema in prod)
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
    return {"message": "Welcome to Airbnb API!"}
