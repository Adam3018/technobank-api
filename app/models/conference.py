"""Conference model for TechnoBank events."""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.database import Base


class Conference(Base):
    """Conference / event information for TechnoBank."""

    __tablename__ = "conferences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    venue = Column(String(255), nullable=True)
    address = Column(String(500), nullable=True)
    organizer = Column(String(255), nullable=True)
    status = Column(String(50), default="draft", nullable=False)
    agenda = Column(JSON, nullable=True)
    visitor_ids = Column(JSON, nullable=True)  # list of invited visitor IDs