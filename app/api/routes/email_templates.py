"""Email template routes."""

import re
import html
from typing import Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from pydantic import BaseModel
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from app.database import get_db

# SQLAlchemy model
from app.models.email_template import EmailTemplate as EmailTemplateModel

# Pydantic schemas
from app.schemas import EmailTemplate, EmailTemplateCreate, EmailTemplateUpdate

from app.crud.email_template import get_email_template, create_email_template, update_email_template, delete_email_template
from app.crud.visitor import get_visitors_by_ids, get_visitor

import logging

from email.message import EmailMessage
import smtplib

# Configure logger
logger = logging.getLogger(__name__)

# SMTP Server Configuration (PUT INTO ENV VARIABLES OR CONFIG FILE IN PRODUCTION)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "adam.adam3018@gmail.com"
SMTP_PASSWORD = "teso jobz gxjy albb"


class PresenterQuestionRequest(BaseModel):
    visitor_id: Optional[int] = None
    visitor_name: Optional[str] = None
    speaker_id: int
    conference_id: Optional[int] = None
    conference_name: Optional[str] = None
    talk_title: str
    question: str


def render_template(body: str, data: dict) -> str:
    """
    Replaces {{key}} in body with values from data dict.
    If a key is missing in data, it defaults to an empty string ''.
    """
    def replace_match(match):
        key = match.group(1).strip()
        return str(data.get(key, ""))

    # Matches anything inside {{ ... }}
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", replace_match, body)


router = APIRouter(prefix="/email-templates", tags=["email-templates"])


@router.get("", response_model=list[EmailTemplate])
def list_email_templates(
    response: Response,
    page: Optional[int] = Query(None, ge=1),
    perPage: Optional[int] = Query(None, ge=1),
    sort: str = Query("id"),
    order: str = Query("ASC"),
    db: Session = Depends(get_db),
):
    query = db.query(EmailTemplateModel)

    total = query.count()

    if hasattr(EmailTemplateModel, sort):
        column = getattr(EmailTemplateModel, sort)
        query = query.order_by(
            asc(column) if order.upper() == "ASC" else desc(column)
        )

    if page and perPage:
        skip = (page - 1) * perPage
        templates = query.offset(skip).limit(perPage).all()

        start = skip
        end = min(skip + len(templates) - 1, total - 1)

        response.headers["Content-Range"] = (
            f"email-templates {start}-{end}/{total}"
        )
        response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    else:
        templates = query.all()
        response.headers["Content-Range"] = (
            f"email-templates 0-{total-1}/{total}"
        )
        response.headers["Access-Control-Expose-Headers"] = "Content-Range"

    return templates

@router.post("", response_model=EmailTemplate, status_code=status.HTTP_201_CREATED)
def create_new_email_template(email_template: EmailTemplateCreate, db: Session = Depends(get_db)):
    return create_email_template(db, email_template)


@router.get("/{email_template_id}", response_model=EmailTemplate)
def read_email_template(email_template_id: int, db: Session = Depends(get_db)):
    db_email_template = get_email_template(db, email_template_id)
    if db_email_template is None:
        raise HTTPException(status_code=404, detail="Email template not found")
    return db_email_template


def send_email_via_smtp(to_email: str, subject: str, body: str):
    """Utility function to send an HTML email via SMTP."""
    try:
        msg = EmailMessage()
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        
        # 1. Provide a plain-text fallback (strips tags or simple message)
        msg.set_content("Please enable HTML in your email client to view this message.")
        
        # 2. Add the actual HTML content
        msg.add_alternative(body, subtype="html")

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            logger.info(f"Email successfully sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")

# Changed decorator from @router.get to @router.post
@router.post("/send/{email_template_id}")
def send_emails(
    email_template_id: int,
    background_tasks: BackgroundTasks,
    visitor_ids: list[int] = Query(..., description="List of visitor IDs to send emails to"),
    db: Session = Depends(get_db)
):
    # 1. Input Validation: Check for empty query parameter list
    if not visitor_ids:
        raise HTTPException(status_code=400, detail="The visitor_ids list cannot be empty.")

    # 2. Fetch Email Template
    db_email_template = get_email_template(db, email_template_id)
    if db_email_template is None:
        raise HTTPException(status_code=404, detail=f"Email template with ID {email_template_id} not found.")

    if not getattr(db_email_template, "body", None) or not getattr(db_email_template, "subject", None):
        raise HTTPException(status_code=422, detail="Email template is missing a required subject or body.")

    # 3. Fetch Visitors matching provided IDs
    db_visitors = get_visitors_by_ids(db, visitor_ids)
    if not db_visitors:
        raise HTTPException(status_code=404, detail="No matching visitors found for the provided IDs.")

    # 4. Render template and validate visitor data
    emails_queued = []
    skipped_visitors = []

    for visitor in db_visitors:
        # Sanitize and safely retrieve fields (fallback to empty string if None/missing)
        recipient = {
            "first_name": getattr(visitor, "first_name", "") or "",
            "last_name": getattr(visitor, "last_name", "") or "",
            "email": getattr(visitor, "email", "") or "",
            "company": getattr(visitor, "company", "") or "",
            "position": getattr(visitor, "position", "") or "",
            "clearance_level": getattr(visitor, "clearance_level", "") or "",
        }

        # Validate core requirement: email address must exist and contain basic structure
        email_addr = recipient["email"].strip()
        if not email_addr or "@" not in email_addr:
            skipped_visitors.append({
                "visitor_id": getattr(visitor, "id", None),
                "reason": "Missing or invalid email address"
            })
            continue

        try:
            formatted_body = render_template(db_email_template.body, recipient)
            formatted_subject = render_template(db_email_template.subject, recipient)
        except Exception as err:
            logger.error(f"Template rendering failed for visitor {getattr(visitor, 'id', 'unknown')}: {err}")
            skipped_visitors.append({
                "visitor_id": getattr(visitor, "id", None),
                "reason": f"Rendering error: {str(err)}"
            })
            continue

        # Add sending task to background processing to prevent HTTP blocking
        background_tasks.add_task(send_email_via_smtp, email_addr, formatted_subject, formatted_body)

        emails_queued.append({
            "to": email_addr,
            "subject": formatted_subject,
        })

    # 5. Check if all items were skipped due to bad data
    if not emails_queued:
        raise HTTPException(
            status_code=422,
            detail={"message": "No emails were queued. All provided visitors lacked valid data.", "skipped": skipped_visitors}
        )

    return {
        "status": "success",
        "template_id": email_template_id,
        "total_queued": len(emails_queued),
        "total_skipped": len(skipped_visitors),
        "queued_emails": emails_queued,
        "skipped": skipped_visitors
    }


@router.post("/send-question")
def send_question_to_presenter(payload: PresenterQuestionRequest, db: Session = Depends(get_db)):
    if not payload.question or not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question text cannot be empty.")

    visitor_name = (payload.visitor_name or '').strip()
    if payload.visitor_id is not None:
        visitor = get_visitor(db, payload.visitor_id)
        if visitor is None:
            raise HTTPException(status_code=404, detail="Visitor not found.")
        visitor_name = (
            f"{getattr(visitor, 'first_name', '')} {getattr(visitor, 'last_name', '')}".strip()
            or visitor_name
            or f"Visitor #{payload.visitor_id}"
        )
    elif not visitor_name:
        raise HTTPException(status_code=400, detail="Visitor name is required when no visitor ID is supplied.")

    presenter = get_visitor(db, payload.speaker_id)
    if presenter is None:
        raise HTTPException(status_code=404, detail="Presenter not found.")

    presenter_email = (getattr(presenter, "email", "") or "").strip()
    if not presenter_email or "@" not in presenter_email:
        raise HTTPException(status_code=400, detail="Presenter email is missing or invalid.")

    if payload.conference_name:
        conference_name = payload.conference_name
    elif payload.conference_id is not None:
        conference_name = f"Conference #{payload.conference_id}"
    else:
        conference_name = "the active conference"

    question_text = html.escape(payload.question.strip())
    talk_title = html.escape(payload.talk_title.strip())
    presenter_name = html.escape(f"{getattr(presenter, 'first_name', '')} {getattr(presenter, 'last_name', '')}".strip())
    visitor_display_name = html.escape(visitor_name)

    subject = f"Question about {payload.talk_title}"
    body = (
        "<html><body>"
        f"<p>Hello {presenter_name},</p>"
        f"<p>You received a question from {visitor_display_name} for <strong>{talk_title}</strong> during {html.escape(conference_name)}.</p>"
        "<p><strong>Question:</strong></p>"
        f"<p>{question_text.replace(chr(10), '<br>')}</p>"
        "</body></html>"
    )

    send_email_via_smtp(presenter_email, subject, body)

    return {
        "status": "success",
        "message": "Question sent to presenter.",
        "presenter_email": presenter_email,
        "talk_title": payload.talk_title,
    }


@router.put("/{email_template_id}", response_model=EmailTemplate)
def update_existing_email_template(email_template_id: int, email_template: EmailTemplateUpdate, db: Session = Depends(get_db)):
    db_email_template = update_email_template(db, email_template_id, email_template)
    if db_email_template is None:
        raise HTTPException(status_code=404, detail="Email template not found")
    return db_email_template

@router.delete("/{email_template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_email_template(email_template_id: int, db: Session = Depends(get_db)):
    success = delete_email_template(db, email_template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Email template not found")
    return None
