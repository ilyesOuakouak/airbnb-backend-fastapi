import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.availability import Availability
from app.schemas.availability import AvailabilityResponse

CACHE_TTL = 30

async def get_availabilities_for_listing_service(
    listing_id: int,
    db: AsyncSession,
    redis
):
    cache_key = f"availability:{listing_id}"

    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    result = await db.execute(
        select(Availability).where(Availability.listing_id == listing_id)
    )
    rows = result.scalars().all()
    data = [AvailabilityResponse.model_validate(r).model_dump(mode="json") for r in rows]

    await redis.setex(cache_key, CACHE_TTL, json.dumps(data))

    return data


async def update_availability_service(
    data,
    db: AsyncSession,
    redis
):
    result = await db.execute(
        select(Availability)
        .where(
            Availability.listing_id == data.listing_id,
            Availability.date == data.date
        )
    )
    existing = result.scalars().first()

    if existing:
        existing.status = data.status
        existing.custom_price = data.custom_price
        existing.checkout_only = data.checkout_only
    else:
        existing = Availability(**data.model_dump())
        db.add(existing)

    await db.commit()
    await db.refresh(existing)

    cache_key = f"availability:{data.listing_id}"
    await redis.delete(cache_key)

    return existing
