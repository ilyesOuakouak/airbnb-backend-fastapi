from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.logging import get_logger
from app.models import Reservation
from app.schemas.reservation import ReservationResponse, ReservationCreate
from opentelemetry import trace
import asyncio

import redis.asyncio as redis
from redis.exceptions import LockError

router = APIRouter(prefix="/reservations", tags=['Reservations'])
logger = get_logger()
tracer = trace.get_tracer(__name__)

# Setup Redis Connection
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

@router.post("/create", response_model=ReservationResponse, status_code=201)
async def create_reservation(
        data: ReservationCreate,
        db: Session = Depends(get_db)
):
    listing_id = data.listing_id
    # DEFINE LOCK KEY
    # Exclusive lock for this specific listing
    lock_key = f"lock:listing:{listing_id}"

    try:
        # ACQUIRED DISTRIBUTED LOCK
        # blocking_timeout=2.0: Wait up to 2 seconds to enter. If busy, Fail.
        # timeout=10.0: (Watchdog) If server crashes, lock auto-releases in 10s.
        async with redis_client.lock(lock_key, blocking_timeout=2.0, timeout=10.0):
            with tracer.start_as_current_span("reservation_critical_section"):
                logger.info(f"✅ Lock acquired for Listing {listing_id}. Checking availability...")
                # 1. CHECK AVAILABILITY
                # We check for ANY reservation that overlaps with the requested dates.
                # Logic: (StartA < EndB) AND (EndA > StartB)
                existing_booking = db.query(Reservation).filter(
                    Reservation.listing_id == listing_id,
                    and_(
                        Reservation.start_date < data.end_date,
                        Reservation.end_date > data.start_date
                    )
                ).first()

                if existing_booking:
                    logger.warning(f"⛔ Race condition caught! Listing {listing_id} is already booked.")
                    raise HTTPException(
                        status_code=409,
                        detail="Dates already booked by another user."
                    )

                # 2. 🐢 SIMULATE WORK
                # This delay previously caused the race condition.
                # Now, it just proves the lock is working (others are forced to wait).
                # await asyncio.sleep(1.0)
                # Since User A holds the lock for 3s, but User B only waits 2s,
                # User B will give up and trigger the LockError (429).
                # await asyncio.sleep(3.0)

                # 3. 📝 CREATE RESERVATION
                new_reservation = Reservation(**data.model_dump())
                db.add(new_reservation)
                db.commit()
                db.refresh(new_reservation)

                logger.success(f"🎉 Securely booked Listing {listing_id} (ID: {new_reservation.id})")
                return new_reservation

    except LockError:
        # This runs if we couldn't get the lock within 2 seconds
        logger.error(f"⏳ Lock Contention: System too busy for Listing {listing_id}")
        raise HTTPException(
            status_code=429,
            detail="System is busy handling other bookings. Please try again."
        )
"""

    with tracer.start_as_current_span("reservation_db_write"):
        # Simulate a slow database or external dependency.
        # This artificial 2-second delay helps us verify that OpenTelemetry captures:
        #   - slow spans,
        #   - end-to-end latency,
        #   - bottlenecks inside the reservation microservice.
        # It appears in Jaeger/Tempo as a long span so we can visually confirm
        # distributed tracing works correctly.
        await asyncio.sleep(0.1)

        new_reservation = Reservation(**data.model_dump())
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)

    return new_reservation
"""

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