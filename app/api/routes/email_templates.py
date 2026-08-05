"""Email template routes."""

import re
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query,
    Response,
)
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from app.database import get_db

# SQLAlchemy model
from app.models.email_template import EmailTemplate as EmailTemplateModel

# Pydantic schemas
from app.schemas import EmailTemplate, EmailTemplateCreate, EmailTemplateUpdate

from app.crud.email_template import get_email_template, create_email_template, update_email_template, delete_email_template
from app.crud.visitor import get_visitors_by_ids

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


@router.get("/send/{email_template_id}")
def send_emails(
    email_template_id: int,
    visitor_ids: list[int] = Query(..., description="List of visitor IDs to send emails to"),
    db: Session = Depends(get_db)
):
    # 1. Fetch Email Template
    db_email_template = get_email_template(db, email_template_id)
    if db_email_template is None:
        raise HTTPException(status_code=404, detail="Email template not found")

    # 2. Fetch Visitors matching the provided IDs
    db_visitors = get_visitors_by_ids(db, visitor_ids)
    if not db_visitors:
        raise HTTPException(status_code=404, detail="No matching visitors found")

    # 3. Render template for each visitor
    emails_to_send = []
    for visitor in db_visitors:
        recipient = {
            "first_name": visitor.first_name,
            "last_name": visitor.last_name,
            "email": visitor.clearance_level,
            "company": visitor.company,
            "position": visitor.position,
        }

        formatted_body = render_template(db_email_template.body, recipient)
        formatted_subject = render_template(db_email_template.subject, recipient)

        emails_to_send.append({
            "to": recipient["email"],
            "subject": formatted_subject,
            "body": formatted_body,
        })

    return {
        "template_id": email_template_id,
        "total_recipients": len(emails_to_send),
        "emails": emails_to_send
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
