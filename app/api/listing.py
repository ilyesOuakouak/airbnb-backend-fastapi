from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.listing import Listing
from app.core.auth import get_current_user
from app.core.database import get_db
from app.schemas.listing import ListingResponse, ListingCreate
from typing import List

router = APIRouter(prefix="/listings", tags=["listings"])

@router.post("/create", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
def create_listing(
        listing: ListingCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    new_listing = Listing(**listing.model_dump(), host_id=current_user.id)
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)

    return new_listing

@router.get("/", response_model=List[ListingResponse])
def get_listings(db: Session = Depends(get_db)):
    return db.query(Listing).all()