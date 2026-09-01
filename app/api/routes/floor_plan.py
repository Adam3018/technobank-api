import os
import uuid

from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
)

router = APIRouter(
    prefix="/floor-plans",
    tags=["floor-plans"]
)

UPLOAD_DIR = Path("uploads/floor_plans")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}


@router.post("/upload")
async def upload_floor_plan(
    file: UploadFile = File(...)
):
    extension = Path(
        file.filename or ""
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PNG, JPG, JPEG and WEBP images are allowed."
        )

    filename = f"{uuid.uuid4()}{extension}"

    destination = UPLOAD_DIR / filename

    contents = await file.read()

    with open(destination, "wb") as buffer:
        buffer.write(contents)

    return {
        "url": f"/uploads/floor_plans/{filename}"
    }