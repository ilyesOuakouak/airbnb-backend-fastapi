import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import get_logger

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.listing import Listing
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.services.reservation_client_service import call_reservation_service

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/create", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation_main(
    data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    logger = get_logger()

    logger.info(
        "📌 Incoming reservation request to MAIN API",
        listing_id=data.listing_id,
        user_id=current_user.id,
        start=data.start_date.isoformat(),
        end=data.end_date.isoformat(),
    )

    listing = db.query(Listing).filter(Listing.id == data.listing_id).first()
    if not listing:
        logger.warning("⚠️ Listing not found", listing_id=data.listing_id)
        raise HTTPException(status_code=404, detail="Listing not found")

    payload = data.model_dump(mode="json")
    payload["user_id"] = current_user.id

    logger.info(
        "➡️ Forwarding reservation request to reservation microservice",
        url=settings.RESERVATION_SERVICE_URL,
        payload=payload
    )

    try:
        response = await call_reservation_service(payload)

        logger.success(
            "✅ Reservation successfully created by reservation microservice",
            microservice_response=response
        )

        return response

    except Exception as e:
        logger.error(
            "❌ Reservation creation failed (microservice error)",
            error=str(e)
        )
        raise