from fastapi import APIRouter, status

from app.schemas.reading import ReadingCreate

router = APIRouter(prefix="/readings", tags=["readings"])


@router.post("", status_code=status.HTTP_201_CREATED)
def ingest_reading(reading: ReadingCreate) -> ReadingCreate:
    # Checkpoint 4 replaces this echo with a database insert.
    return reading