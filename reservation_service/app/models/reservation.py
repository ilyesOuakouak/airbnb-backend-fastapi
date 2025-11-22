
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.core.database import Base


class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="pending")