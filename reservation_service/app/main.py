from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.api import reservation
from app.core.database import Base, sync_engine
from app.core.logging import get_logger
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.tracing import init_tracer

# -----------------------------
# OpenTelemetry imports
# -----------------------------

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import context
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.propagate import extract



logger = get_logger()
tracer_provider = init_tracer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 main_api service started (lifespan)")

    yield  # ← App runs here

    # Shutdown
    logger.info("🛑 main_api service stopped (lifespan)")

app = FastAPI(
    title="Reservation Microservice",
    lifespan=lifespan
)

# 🔑 IMPORTANT: attach incoming trace context from headers
@app.middleware("http")
async def otel_context_middleware(request: Request, call_next):
    # Extract context from W3C trace headers (traceparent, tracestate)
    ctx = extract(request.headers)
    token = context.attach(ctx)
    try:
        response = await call_next(request)
        return response
    finally:
        context.detach(token)


# Auto-instrument FastAPI (server spans)
FastAPIInstrumentor().instrument_app(app, tracer_provider=tracer_provider)

# Instrument SQLAlchemy (DB spans use propagated context)
SQLAlchemyInstrumentor().instrument(
    engine=sync_engine,
    tracer_provider=tracer_provider,
)

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
