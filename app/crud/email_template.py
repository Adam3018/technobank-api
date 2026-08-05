"""CRUD operations for EmailTemplate."""

from sqlalchemy.orm import Session
from app.models import EmailTemplate
from app.schemas import EmailTemplateCreate, EmailTemplateUpdate


def get_email_template(db: Session, email_template_id: int) -> EmailTemplate | None:
    return db.query(EmailTemplate).filter(EmailTemplate.id == email_template_id).first()


def get_email_templates(db: Session, skip: int = 0, limit: int = 100) -> list[EmailTemplate]:
    return db.query(EmailTemplate).offset(skip).limit(limit).all()


def create_email_template(db: Session, email_template: EmailTemplateCreate) -> EmailTemplate:
    db_email_template = EmailTemplate(**email_template.model_dump())
    db.add(db_email_template)
    db.commit()
    db.refresh(db_email_template)
    return db_email_template


def update_email_template(db: Session, email_template_id: int, email_template: EmailTemplateUpdate) -> EmailTemplate | None:
    db_email_template = db.query(EmailTemplate).filter(EmailTemplate.id == email_template_id).first()
    if db_email_template:
        update_data = email_template.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_email_template, key, value)
        db.add(db_email_template)
        db.commit()
        db.refresh(db_email_template)
    return db_email_template


def send_emails(db: Session, email_template_id: int) -> EmailTemplate | None:
    return db.query(EmailTemplate).filter(EmailTemplate.id == email_template_id).first()

 
def delete_email_template(db: Session, email_template_id: int) -> bool:
    db_email_template = db.query(EmailTemplate).filter(EmailTemplate.id == email_template_id).first()
    if db_email_template:
        db.delete(db_email_template)
        db.commit()
        return True
    return False
