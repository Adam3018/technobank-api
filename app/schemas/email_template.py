"""Pydantic schemas for email templates."""

from typing import Optional
from pydantic import BaseModel, Field


class EmailTemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    subject: str = Field(..., min_length=1, max_length=500)
    body: str = Field(..., min_length=1)
    placeholder_help: Optional[str] = None
    is_active: bool = True


class EmailTemplateCreate(EmailTemplateBase):
    pass


class EmailTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    subject: Optional[str] = Field(None, min_length=1, max_length=500)
    body: Optional[str] = Field(None, min_length=1)
    placeholder_help: Optional[str] = None
    is_active: Optional[bool] = None


class EmailTemplate(EmailTemplateBase):
    id: int

    class Config:
        from_attributes = True
