"""Email template model for sending invitations and updates."""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from app.database import Base


class EmailTemplate(Base):
    """Reusable email template for conference communications."""

    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    placeholder_help = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
