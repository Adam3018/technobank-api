"""Email template routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import EmailTemplate, EmailTemplateCreate, EmailTemplateUpdate
from app.crud import get_email_template, get_email_templates, create_email_template, update_email_template, delete_email_template

router = APIRouter(prefix="/email-templates", tags=["email-templates"])


@router.get("", response_model=list[EmailTemplate])
def list_email_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_email_templates(db, skip=skip, limit=limit)


@router.post("", response_model=EmailTemplate, status_code=status.HTTP_201_CREATED)
def create_new_email_template(email_template: EmailTemplateCreate, db: Session = Depends(get_db)):
    return create_email_template(db, email_template)


@router.get("/{email_template_id}", response_model=EmailTemplate)
def read_email_template(email_template_id: int, db: Session = Depends(get_db)):
    db_email_template = get_email_template(db, email_template_id)
    if db_email_template is None:
        raise HTTPException(status_code=404, detail="Email template not found")
    return db_email_template


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
