"""CRUD operations for Visitor."""

from sqlalchemy.orm import Session
from app.models import Visitor
from app.schemas import VisitorCreate, VisitorUpdate


def get_visitor(db: Session, visitor_id: int) -> Visitor | None:
    return db.query(Visitor).filter(Visitor.id == visitor_id).first()


def get_visitors(db: Session, skip: int = 0, limit: int = 100) -> list[Visitor]:
    return db.query(Visitor).offset(skip).limit(limit).all()

def get_visitors_by_ids(db: Session, visitor_ids: list[int]) -> list[Visitor]:
    """Retrieve multiple visitors matching a list of IDs."""
    if not visitor_ids:
        return []
    return db.query(Visitor).filter(Visitor.id.in_(visitor_ids)).all()

def create_visitor(db: Session, visitor: VisitorCreate) -> Visitor:
    db_visitor = Visitor(**visitor.model_dump())
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor


def update_visitor(db: Session, visitor_id: int, visitor: VisitorUpdate) -> Visitor | None:
    db_visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if db_visitor:
        update_data = visitor.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_visitor, key, value)
        db.add(db_visitor)
        db.commit()
        db.refresh(db_visitor)
    return db_visitor


def delete_visitor(db: Session, visitor_id: int) -> bool:
    db_visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if db_visitor:
        db.delete(db_visitor)
        db.commit()
        return True
    return False
