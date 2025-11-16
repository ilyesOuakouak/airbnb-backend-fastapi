
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Listing(Base):
    __tablename__ = "listing"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    price_per_night = Column(Float, nullable=False)
    host_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    host = relationship("User", back_populates="listings")
    availabilities = relationship("Availability", back_populates="listing", cascade="all, delete-orphan")
    rentals = relationship("Rental", back_populates="listing", cascade="all, delete-orphan")
