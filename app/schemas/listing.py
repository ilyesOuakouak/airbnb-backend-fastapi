from typing import Optional
from pydantic import BaseModel, constr


class ListingBase(BaseModel):
    title: constr(min_length=10, max_length=255)
    description: Optional[str]
    price_per_night: float

class ListingCreate(ListingBase):
    pass

class ListingResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price_per_night: float
    host_id: int

    class Config:
        from_attributes = True