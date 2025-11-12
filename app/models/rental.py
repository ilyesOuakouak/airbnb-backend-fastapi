
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Rental(Base):
    __tablename__ = "rental"
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listing.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    amount_from_host = Column(Float, nullable=True)
    amount_from_guest = Column(Float, nullable=True)
    is_validated = Column(Boolean, default=False)

    listing = relationship("Listing", back_populates="rentals")
    user = relationship("User", back_populates="rentals")