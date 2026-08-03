"""Pydantic schemas for visitors."""

from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class VisitorBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=150)
    last_name: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    company: Optional[str] = Field(None, max_length=255)
    position: Optional[str] = Field(None, max_length=255)
    clearance_level: str = Field(default="visitor", max_length=50)
    phone: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=1000)
    is_active: bool = True


class VisitorCreate(VisitorBase):
    pass


class VisitorUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=150)
    last_name: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = None
    company: Optional[str] = Field(None, max_length=255)
    position: Optional[str] = Field(None, max_length=255)
    clearance_level: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None


class Visitor(VisitorBase):
    id: int

    class Config:
        from_attributes = True
