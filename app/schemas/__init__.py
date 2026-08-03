"""
Pydantic schemas for request/response validation
"""

from .conference import ConferenceBase, ConferenceCreate, ConferenceUpdate, Conference
from .email_template import EmailTemplateBase, EmailTemplateCreate, EmailTemplateUpdate, EmailTemplate
from .visitor import VisitorBase, VisitorCreate, VisitorUpdate, Visitor

__all__ = [
    "ConferenceBase",
    "ConferenceCreate",
    "ConferenceUpdate",
    "Conference",
    "EmailTemplateBase",
    "EmailTemplateCreate",
    "EmailTemplateUpdate",
    "EmailTemplate",
    "VisitorBase",
    "VisitorCreate",
    "VisitorUpdate",
    "Visitor",
]
