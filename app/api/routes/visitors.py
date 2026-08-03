"""Visitor routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Visitor, VisitorCreate, VisitorUpdate
from app.crud import get_visitor, get_visitors, create_visitor, update_visitor, delete_visitor

router = APIRouter(prefix="/visitors", tags=["visitors"])


@router.get("", response_model=list[Visitor])
def list_visitors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_visitors(db, skip=skip, limit=limit)


@router.post("", response_model=Visitor, status_code=status.HTTP_201_CREATED)
def create_new_visitor(visitor: VisitorCreate, db: Session = Depends(get_db)):
    return create_visitor(db, visitor)


@router.get("/{visitor_id}", response_model=Visitor)
def read_visitor(visitor_id: int, db: Session = Depends(get_db)):
    db_visitor = get_visitor(db, visitor_id)
    if db_visitor is None:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return db_visitor


@router.put("/{visitor_id}", response_model=Visitor)
def update_existing_visitor(visitor_id: int, visitor: VisitorUpdate, db: Session = Depends(get_db)):
    db_visitor = update_visitor(db, visitor_id, visitor)
    if db_visitor is None:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return db_visitor


@router.delete("/{visitor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_visitor(visitor_id: int, db: Session = Depends(get_db)):
    success = delete_visitor(db, visitor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return None
