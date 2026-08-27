"""Visitor routes."""

import json
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Query,
    Response,
)
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from rapidfuzz import fuzz

import io
import pandas as pd

from app.database import get_db

# SQLAlchemy model
from app.models.visitor import Visitor as VisitorModel

# Pydantic schemas
from app.schemas import Visitor, VisitorCreate, VisitorUpdate

from app.crud import (
    get_visitor,
    create_visitor,
    update_visitor,
    delete_visitor,
)

router = APIRouter(prefix="/visitors", tags=["visitors"])

FUZZY_THRESHOLD = 60  # 0-100, lower = more forgiving of typos


def _fuzzy_matches(visitor: VisitorModel, name: str | None, company: str | None) -> bool:
    if name:
        full_name = f"{visitor.first_name} {visitor.last_name}"
        if fuzz.partial_ratio(name.lower(), full_name.lower()) <= FUZZY_THRESHOLD:
            return False
    if company:
        if fuzz.partial_ratio(company.lower(), (visitor.company or "").lower()) <= FUZZY_THRESHOLD:
            return False
    return True


@router.get("", response_model=list[Visitor])
def list_visitors(
    response: Response,
    page: Optional[int] = Query(None, ge=1),
    perPage: Optional[int] = Query(None, ge=1),
    sort: str = Query("id"),
    order: str = Query("ASC"),
    filter: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    # Parse filter JSON sent by React Admin, e.g. {"name":"jon","company":"acme"}
    filters = json.loads(filter) if filter else {}
    name_filter = filters.get("name")
    company_filter = filters.get("company")

    query = db.query(VisitorModel)

    # Dynamic Sorting (applied before fuzzy filtering so it still works on the base query)
    field_map = {
        "clearance": "clearance_level",
        "firstName": "first_name",
        "lastName": "last_name"
    }
    target_field = field_map.get(sort, sort)

    if hasattr(VisitorModel, target_field):
        column = getattr(VisitorModel, target_field)
        sort_column = asc(column) if order.upper() == "ASC" else desc(column)
        query = query.order_by(sort_column)
    else:
        query = query.order_by(asc(VisitorModel.id))

    if name_filter or company_filter:
        # Fuzzy matching happens in Python, so pull the (sorted) candidates first
        all_visitors = query.all()
        matched = [v for v in all_visitors if _fuzzy_matches(v, name_filter, company_filter)]
        total_count = len(matched)

        if page is not None and perPage is not None:
            skip = (page - 1) * perPage
            visitors = matched[skip:skip + perPage]
            start = skip
            end = min(skip + len(visitors) - 1, total_count - 1) if total_count > 0 else 0
        else:
            visitors = matched
            start = 0
            end = total_count - 1 if total_count > 0 else 0

        response.headers["Content-Range"] = f"visitors {start}-{end}/{total_count}"
        response.headers["Access-Control-Expose-Headers"] = "Content-Range"
        return visitors

    # No name/company filter -> original behavior, unchanged
    total_count = query.count()

    if page is not None and perPage is not None:
        skip = (page - 1) * perPage
        visitors = query.offset(skip).limit(perPage).all()
        start = skip
        end = min(skip + len(visitors) - 1, total_count - 1) if total_count > 0 else 0
        response.headers["Content-Range"] = f"visitors {start}-{end}/{total_count}"
        response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    else:
        visitors = query.all()
        response.headers["Content-Range"] = f"visitors 0-{total_count-1}/{total_count}"
        response.headers["Access-Control-Expose-Headers"] = "Content-Range"

    return visitors


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


@router.delete("/{visitor_id}", status_code=status.HTTP_200_OK)
def delete_existing_visitor(visitor_id: int, db: Session = Depends(get_db)):
    success = delete_visitor(db, visitor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return {"id": visitor_id}


@router.post("/import")
async def import_visitors(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    filename = file.filename.lower()
    contents = await file.read()
    
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload CSV or Excel.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    df = df.astype(object).where(pd.notnull(df), None)
    
    imported_count = 0
    records = df.to_dict(orient="records")

    def clean_val(val):
        if val is None or pd.isna(val):
            return None
        s = str(val).strip()
        return s if s != "" else None

    for row_number, row in enumerate(records, start=2):
        try:
            first_name = clean_val(row.get("First Name") or row.get("first_name"))
            last_name = clean_val(row.get("Last Name") or row.get("last_name"))
            email = clean_val(row.get("Email") or row.get("email"))
            company = clean_val(row.get("Company") or row.get("company"))
            position = clean_val(row.get("Position") or row.get("position"))
            clearance = clean_val(
                row.get("Clearance")
                or row.get("clearance")
                or row.get("clearance_level")
            ) or "visitor"
            phone = clean_val(row.get("Phone") or row.get("phone"))
            notes = clean_val(row.get("Notes") or row.get("notes"))

            visitor_in = VisitorCreate(
                first_name=first_name or "",
                last_name=last_name or "",
                email=email or "",
                company=company,
                position=position,
                clearance_level=clearance,
                phone=phone,
                notes=notes,
            )

            create_visitor(db, visitor_in)

            imported_count += 1

        except Exception as e:
            db.rollback()
            print(f"Skipping row {row_number}: {e}")
            continue

    return {
        "message": "Import completed",
        "imported_count": imported_count,
        "skipped_count": len(records) - imported_count,
    }