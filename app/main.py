from fastapi import FastAPI
from app.core.database import Base, sync_engine
import app.models

from app.api import user, listing, availability, reservation

app = FastAPI(title="AirBnb Backend")

# Register routers
app.include_router(user.router)
app.include_router(listing.router)
app.include_router(availability.router)
app.include_router(reservation.router)

# Temporary: auto-create tables for development (Alembic handles schema in prod)
Base.metadata.create_all(bind=sync_engine)

@app.get("/")
def root():
    return {"message": "Welcome to Airbnb API!"}
