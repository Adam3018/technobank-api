"""
Route modules
"""

from fastapi import APIRouter
from .conferences import router as conferences_router
from .email_templates import router as email_templates_router
from .visitors import router as visitors_router

router = APIRouter()
router.include_router(conferences_router)
router.include_router(email_templates_router)
router.include_router(visitors_router)

__all__ = ["router"]
