"""Conference routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Conference, ConferenceCreate, ConferenceUpdate
from app.crud import get_conference, get_conferences, create_conference, update_conference, delete_conference
from fastapi import UploadFile, File
from pathlib import Path
from uuid import uuid4

router = APIRouter(prefix="/conferences", tags=["conferences"])

UPLOAD_DIR = Path("uploads/floor_plans")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.get("", response_model=list[Conference])
def list_conferences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_conferences(db, skip=skip, limit=limit)


@router.post("", response_model=Conference, status_code=status.HTTP_201_CREATED)
def create_new_conference(conference: ConferenceCreate, db: Session = Depends(get_db)):
    return create_conference(db, conference)


@router.get("/{conference_id}", response_model=Conference)
def read_conference(conference_id: int, db: Session = Depends(get_db)):
    db_conference = get_conference(db, conference_id)
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")
    return db_conference


@router.put("/{conference_id}", response_model=Conference)
def update_existing_conference(conference_id: int, conference: ConferenceUpdate, db: Session = Depends(get_db)):
    db_conference = update_conference(db, conference_id, conference)
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")
    return db_conference


@router.delete("/{conference_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_conference(conference_id: int, db: Session = Depends(get_db)):
    success = delete_conference(db, conference_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conference not found")
    return None


@router.post("/{conference_id}/floor-plan")
async def upload_floor_plan(
    conference_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    conference = (
        db.query(Conference)
        .filter(Conference.id == conference_id)
        .first()
    )

    if conference is None:
        raise HTTPException(
            status_code=404,
            detail="Conference not found"
        )

    allowed_types = {
        "image/png",
        "image/jpeg",
        "image/webp",
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPEG and WebP images are allowed"
        )

    extension = Path(
        file.filename or ""
    ).suffix.lower()

    filename = (
        f"conference_{conference_id}_"
        f"{uuid4().hex}{extension}"
    )

    file_path = UPLOAD_DIR / filename

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    image_url = f"/uploads/floor_plans/{filename}"

    conference.floor_plan_image = image_url

    db.commit()
    db.refresh(conference)

    return {
        "floor_plan_image": image_url
    }