

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models import Listing, Availability
from app.schemas.availability import AvailabilityResponse, AvailabilityUpdate

router = APIRouter(prefix="/availabilities", tags=["availabilities"])

@router.get("/{listing_id}", response_model=list[AvailabilityResponse], status_code=status.HTTP_200_OK)
def get_availabilities(listing_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    availabilities = db.query(Availability).filter(Availability.listing_id == listing_id).all()

    return availabilities

@router.post("/update", response_model=AvailabilityResponse, status_code=status.HTTP_201_CREATED)
def update_availability(
    data: AvailabilityUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    listing = db.query(Listing).filter(Listing.id == data.listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    availability = (
        db.query(Availability)
        .filter(Availability.listing_id == data.listing_id, Availability.date == data.date)
        .first()
    )

    if availability:
        availability.status = data.status
        availability.custom_price = data.custom_price
        availability.checkout_only = data.checkout_only
    else:
        availability = Availability(**data.model_dump())
        db.add(availability)

    db.commit()
    db.refresh(availability)
    return availability

