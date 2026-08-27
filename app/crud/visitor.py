"""CRUD operations for Visitor."""

from sqlalchemy.orm import Session
from rapidfuzz import fuzz
from app.models import Visitor
from app.schemas import VisitorCreate, VisitorUpdate


def get_visitor(db: Session, visitor_id: int) -> Visitor | None:
    return db.query(Visitor).filter(Visitor.id == visitor_id).first()


def get_visitors(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str | None = None,
    company: str | None = None,
) -> list[Visitor]:
    query = db.query(Visitor)

    if name or company:
        all_rows = query.all()
        scored = []
        for v in all_rows:
            ok = True
            if name:
                full_name = f"{v.first_name} {v.last_name}"
                ok = ok and fuzz.partial_ratio(name.lower(), full_name.lower()) > 60
            if company:
                ok = ok and fuzz.partial_ratio(company.lower(), (v.company or "").lower()) > 60
            if ok:
                scored.append(v)
        return scored[skip:skip + limit]

    return query.offset(skip).limit(limit).all()


def get_visitors_count(
    db: Session,
    name: str | None = None,
    company: str | None = None,
) -> int:
    """Total count for the same filter, needed for React Admin's Content-Range header."""
    query = db.query(Visitor)

    if name or company:
        all_rows = query.all()
        count = 0
        for v in all_rows:
            ok = True
            if name:
                full_name = f"{v.first_name} {v.last_name}"
                ok = ok and fuzz.partial_ratio(name.lower(), full_name.lower()) > 60
            if company:
                ok = ok and fuzz.partial_ratio(company.lower(), (v.company or "").lower()) > 60
            if ok:
                count += 1
        return count

    return query.count()


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