from fastapi import FastAPI
from app.api import reservation
from app.core.database import Base, sync_engine

app = FastAPI(title="Reservation Microservice")
app.include_router(reservation.router)

Base.metadata.create_all(bind=sync_engine)

@app.get("/")
def root():
    return {"service": "reservation", "status": "running"}
