import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

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
    listing = db.query(Listing).filter(Listing.id == data.listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    payload = data.model_dump(mode="json")
    payload["user_id"] = current_user.id

    return await call_reservation_service(payload)