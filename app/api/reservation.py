from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.reservation import Reservation
from app.models.listing import Listing
from app.schemas.reservation import ReservationCreate, ReservationResponse

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/create", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    listing = db.query(Listing).filter(Listing.id == reservation.listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    new_reservation = Reservation(**reservation.model_dump(), user_id=current_user.id)
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation


@router.get("/my", response_model=list[ReservationResponse])
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Reservation).filter(Reservation.user_id == current_user.id).all()


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id,
        Reservation.user_id == current_user.id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reservation.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending reservations can be cancelled")

    db.delete(reservation)
    db.commit()
