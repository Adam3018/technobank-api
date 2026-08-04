"""Visitor model for conference attendees and participants."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.database import Base


class Visitor(Base):
    """Visitor / attendee profile for a conference."""

    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(150), nullable=False, index=True)
    last_name = Column(String(150), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    company = Column(String(255), nullable=True)
    position = Column(String(255), nullable=True)
    clearance_level = Column(String(50), nullable=False, default="visitor")
    phone = Column(String(50), nullable=True)
    notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
