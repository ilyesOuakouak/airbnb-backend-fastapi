

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_current_user
from app.core.database import get_db, get_async_db
from app.core.redis_client import get_redis

from app.models import Listing, Availability
from app.schemas.availability import AvailabilityResponse, AvailabilityUpdate
from app.services.availability_service import get_availabilities_for_listing_service, update_availability_service

router = APIRouter(prefix="/availabilities", tags=["availabilities"])

@router.get("/{listing_id}", response_model=list[AvailabilityResponse], status_code=status.HTTP_200_OK)
async def get_availabilities(
    listing_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
    redis=Depends(get_redis)
):
    return await get_availabilities_for_listing_service(listing_id, db, redis)


@router.post("/update", response_model=AvailabilityResponse, status_code=status.HTTP_201_CREATED)
async def update_availability(
    data: AvailabilityUpdate,
    db: AsyncSession = Depends(get_async_db),
    redis=Depends(get_redis),
    current_user=Depends(get_current_user)
):
    return  await update_availability_service(data, db, redis)

