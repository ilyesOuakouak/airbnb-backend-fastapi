from datetime import date
from pydantic import BaseModel
from typing import Optional



class ReservationBase(BaseModel):
    listing_id: int
    start_date: date
    end_date: date
    total_amount: Optional[float]


class ReservationCreate(BaseModel):
    listing_id: int
    user_id: int
    start_date: date
    end_date: date
    total_amount: Optional[float]


class ReservationResponse(ReservationBase):
    id: int
    status: str

    class Config:
        from_attributes = True