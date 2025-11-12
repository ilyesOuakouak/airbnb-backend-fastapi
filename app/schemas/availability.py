from datetime import date
from typing import Optional

from pydantic import BaseModel, constr

class AvailabilityBase(BaseModel):
    date: date
    status: constr(min_length=3, max_length=20)
    custom_price: Optional[float] = None
    checkout_only: Optional[bool] = False

class AvailabilityUpdate(AvailabilityBase):
    listing_id: int

class AvailabilityResponse(AvailabilityBase):
    id: int
    listing_id: int

    class Config:
        from_attributes = True