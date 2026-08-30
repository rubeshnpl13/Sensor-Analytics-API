from fastapi import APIRouter, status

from app.core.db import SessionDep
from app.schemas.reading import ReadingCreate, ReadingOut
from app.services import readings as readings_service

router = APIRouter(prefix="/readings", tags=["readings"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def ingest_reading(reading: ReadingCreate, session: SessionDep) -> ReadingOut:
    return await readings_service.ingest(session, reading)