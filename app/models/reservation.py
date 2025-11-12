
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listing.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="pending")
    total_amount = Column(Float, nullable=False)

    listing = relationship("Listing", back_populates="reservations")
    user = relationship("User", back_populates="reservations")