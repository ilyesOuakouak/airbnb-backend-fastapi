# app/services/reservation_client_service.py
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
from fastapi import HTTPException
from app.core.config import settings

from app.core.circuit_breaker import CircuitBreaker
from opentelemetry import trace

RESERVATION_SERVICE_URL = "http://reservation_api:8001"
breaker = CircuitBreaker()
tracer = trace.get_tracer(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=0.1, max=1),
)
async def _post_to_reservation_service(payload: dict):
    url = f"{settings.RESERVATION_SERVICE_URL}/reservations/create"
    async with httpx.AsyncClient() as client:
        return await client.post(
            url,
            json=payload,
            timeout=5.0,
        )


async def call_reservation_service(payload: dict) -> dict:
    # 1) Circuit breaker check
    if not breaker.allow_request():
        raise HTTPException(
            status_code=503,
            detail="Reservation service temporarily unavailable (circuit open)",
        )

    try:
        with tracer.start_as_current_span("call_reservation_microservice"):
            response = await _post_to_reservation_service(payload)
    except RetryError:
        breaker.record_failure()
        raise HTTPException(
            status_code=504,
            detail="Reservation service unreachable after retries",
        )

    # 2) Remote error
    if response.status_code >= 500:
        breaker.record_failure()
    else:
        breaker.record_success()

    if response.status_code != 201:
        raise HTTPException(response.status_code, detail=response.text)

    return response.json()
