"""Pydantic schemas for conferences."""

from datetime import date, time
from typing import Optional
from pydantic import BaseModel, Field


class ConferenceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    short_name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    conference_date: date
    start_time: time
    end_time: Optional[time] = None
    venue: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=500)
    organizer: Optional[str] = Field(None, max_length=255)
    status: str = Field(default="draft", max_length=50)
    is_public: bool = True
    max_attendees: Optional[int] = Field(None, ge=1)
    notes: Optional[str] = None


class ConferenceCreate(ConferenceBase):
    pass


class ConferenceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    short_name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    conference_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    venue: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=500)
    organizer: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, max_length=50)
    is_public: Optional[bool] = None
    max_attendees: Optional[int] = Field(None, ge=1)
    notes: Optional[str] = None


class Conference(ConferenceBase):
    id: int

    class Config:
        from_attributes = True
