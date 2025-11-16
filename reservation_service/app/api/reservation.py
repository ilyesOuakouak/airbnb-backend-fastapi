from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Reservation
from app.schemas.reservation import ReservationResponse, ReservationCreate

router = APIRouter(prefix="/reservations", tags=['Reservations'])

@router.post("/create", response_model=ReservationResponse, status_code=201)
def create_reservation(
        data: ReservationCreate,
        db: Session = Depends(get_db)
):
    new_reservation = Reservation(**data.model_dump())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation

@router.get("/listing/{listing_id}", response_model=list[ReservationResponse])
def get_reservations_by_listing(listing_id: int, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.listing_id == listing_id).all()


@router.get("/user/{user_id}", response_model=list[ReservationResponse])
def get_reservations_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.user_id == user_id).all()


@router.delete("/{reservation_id}")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    res = db.query(Reservation).filter(Reservation.id == reservation_id).first()

    if not res:
        raise HTTPException(404, "Reservation not found")

    db.delete(res)
    db.commit()
    return {"message": "Deleted"}