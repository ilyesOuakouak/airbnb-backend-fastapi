from app.api import user, listing, availability, reservation
from fastapi import FastAPI
from app.core.database import Base, engine
import app.models
app = FastAPI(title="AirBnb Backend")

app.include_router(user.router)
app.include_router(listing.router)
app.include_router(availability.router)
app.include_router(reservation.router)
# Temporary: create tables automatically (we’ll replace this with Alembic soon)
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to Airbnb API!"}
