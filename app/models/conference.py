"""Conference model for TechnoBank events."""

from sqlalchemy import Column, Integer, String, Text, Date, Time, Boolean
from app.database import Base


class Conference(Base):
    """Conference / event information for TechnoBank."""

    __tablename__ = "conferences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    short_name = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    conference_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=True)
    venue = Column(String(255), nullable=True)
    address = Column(String(500), nullable=True)
    organizer = Column(String(255), nullable=True)
    status = Column(String(50), default="draft", nullable=False)
    is_public = Column(Boolean, default=True)
    max_attendees = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
