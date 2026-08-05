"""Visitor routes."""

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

# @router.get("", response_model=list[Visitor])
# def list_visitors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return get_visitors(db, skip=skip, limit=limit)

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
    query = db.query(VisitorModel)
    total_count = query.count()

    # Dynamic Sorting
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

    # Check if pagination parameters are provided
    if page is not None and perPage is not None:
        skip = (page - 1) * perPage
        visitors = query.offset(skip).limit(perPage).all()
        
        # Set React Admin Content-Range header for pagination
        start = skip
        end = min(skip + len(visitors) - 1, total_count - 1) if total_count > 0 else 0
        response.headers["Content-Range"] = f"visitors {start}-{end}/{total_count}"
        response.headers["Access-Control-Expose-Headers"] = "Content-Range"
    else:
        # Return ALL records if page/perPage are not supplied
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

    # Replace all NaN / NaT values with None explicitly across the DataFrame
    df = df.astype(object).where(pd.notnull(df), None)
    
    imported_count = 0
    records = df.to_dict(orient="records")

    # Helper function to sanitize cell values and prevent NaN leaking to Pydantic
    def clean_val(val):
        if val is None or pd.isna(val):
            return None
        s = str(val).strip()
        return s if s != "" else None

    for row in records:
        # Extract and clean values safely
        first_name = clean_val(row.get("First Name") or row.get("first_name"))
        last_name = clean_val(row.get("Last Name") or row.get("last_name"))
        email = clean_val(row.get("Email") or row.get("email"))
        company = clean_val(row.get("Company") or row.get("company"))
        position = clean_val(row.get("Position") or row.get("position"))
        clearance = clean_val(row.get("Clearance") or row.get("clearance") or row.get("clearance_level")) or "visitor"
        phone = clean_val(row.get("Phone") or row.get("phone"))
        notes = clean_val(row.get("Notes") or row.get("notes"))

        # Create Pydantic schema safely
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
        
        # Save to database
        create_visitor(db, visitor_in)
        imported_count += 1

    return {"message": "Import successful", "imported_count": imported_count}