"""Pydantic schemas for conferences."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class AgendaItem(BaseModel):
    speaker_id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=255)
    start_time: str
    end_time: Optional[str] = None
    type: str = Field(default="talk", max_length=50)


class ConferenceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    venue: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=500)
    organizer: Optional[str] = Field(None, max_length=255)
    status: str = Field(default="draft", max_length=50)
    agenda: Optional[List[AgendaItem]] = None
    visitor_ids: Optional[List[int]] = []


class ConferenceCreate(ConferenceBase):
    pass


class ConferenceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    venue: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=500)
    organizer: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, max_length=50)
    agenda: Optional[List[AgendaItem]] = None
    visitor_ids: Optional[List[int]] = None


class Conference(ConferenceBase):
    id: int

    class Config:
        from_attributes = True