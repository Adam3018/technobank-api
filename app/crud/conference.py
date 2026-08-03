"""CRUD operations for Conference."""

from sqlalchemy.orm import Session
from app.models import Conference
from app.schemas import ConferenceCreate, ConferenceUpdate


def get_conference(db: Session, conference_id: int) -> Conference | None:
    return db.query(Conference).filter(Conference.id == conference_id).first()


def get_conferences(db: Session, skip: int = 0, limit: int = 100) -> list[Conference]:
    return db.query(Conference).offset(skip).limit(limit).all()


def create_conference(db: Session, conference: ConferenceCreate) -> Conference:
    db_conference = Conference(**conference.model_dump())
    db.add(db_conference)
    db.commit()
    db.refresh(db_conference)
    return db_conference


def update_conference(db: Session, conference_id: int, conference: ConferenceUpdate) -> Conference | None:
    db_conference = db.query(Conference).filter(Conference.id == conference_id).first()
    if db_conference:
        update_data = conference.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_conference, key, value)
        db.add(db_conference)
        db.commit()
        db.refresh(db_conference)
    return db_conference


def delete_conference(db: Session, conference_id: int) -> bool:
    db_conference = db.query(Conference).filter(Conference.id == conference_id).first()
    if db_conference:
        db.delete(db_conference)
        db.commit()
        return True
    return False
