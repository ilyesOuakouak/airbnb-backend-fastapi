
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Availability(Base):
    __tablename__ = "availability"
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listing.id"), nullable=False)

    date = Column(DateTime, nullable=False)
    status = Column(String(50), default="available")  # available, booked, blocked, cancelled
    custom_price = Column(Float, nullable=True)
    checkout_only = Column(Boolean, default=False)

    listing = relationship("Listing", back_populates="availabilities")